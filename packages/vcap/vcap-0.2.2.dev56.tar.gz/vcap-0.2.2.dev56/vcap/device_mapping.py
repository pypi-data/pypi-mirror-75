import os
import logging
from threading import RLock
from typing import Callable, List

import tensorflow as tf
from tensorflow.python.client import device_lib

_devices = None
_devices_lock = RLock()


def get_all_devices() -> List[str]:
    """Returns a list of devices in the computer. Example:
    ['CPU:0', 'XLA_GPU:0', 'XLA_CPU:0', 'GPU:0', 'GPU:1', 'GPU:2', 'GPU:3']
    """
    global _devices, _devices_lock

    # Initialize the device list if necessary
    with _devices_lock:
        if _devices is None:
            # We set these config options on the session because otherwise list
            # local_devices allocates all of the available GPU memory to the
            # computer
            #
            # Note that this config has the side effect of being set for all
            # future sessions#
            #
            # TODO: Use tf.config.list_physical_devices in TF 2.1
            # TODO: Remove the config when using TF_FORCE_GPU_ALLOW_GROWTH\
            #  environment variable
            _process_gpu_options = tf.GPUOptions(allow_growth=True)
            config = tf.ConfigProto(gpu_options=_process_gpu_options)

            with tf.Session(config=config):
                all_devices = device_lib.list_local_devices()

            # Get the device names and remove duplicates, just in case...
            tf_discovered_devices = {
                d.name.replace("/device:", "")
                for d in all_devices
            }

            # Discover devices using OpenVINO
            try:
                from openvino.inference_engine import IECore
                ie = IECore()
                openvino_discovered_devices = {
                    d for d in ie.available_devices
                    if not d.lower().startswith("cpu")
                }
            except ModuleNotFoundError:
                logging.warning("OpenVINO library not found. "
                                "OpenVINO devices will not be discovered. ")
                openvino_discovered_devices = set()
            _devices = list(tf_discovered_devices
                            | openvino_discovered_devices)
    return _devices


class DeviceMapper:
    def __init__(self, filter_func: Callable[[List[str]], List[str]]):
        """The filter will take in a list of devices formatted as
        ["CPU:0", "CPU:1", "GPU:0", "GPU:1"], etc and output a filtered list of
        devices.
        """
        self.filter_func = filter_func

    @staticmethod
    def map_to_all_gpus(cpu_fallback=True) -> 'DeviceMapper':
        def filter_func(devices):
            gpu_devices = [d for d in devices if d.startswith("GPU:")]
            if not gpu_devices and cpu_fallback:
                return ["CPU:0"]
            return gpu_devices

        return DeviceMapper(filter_func=filter_func)

    @staticmethod
    def map_to_single_cpu() -> 'DeviceMapper':
        def filter_func(devices):
            return [next(d for d in devices if d.startswith("CPU:"))]

        return DeviceMapper(filter_func=filter_func)

    @staticmethod
    def map_to_openvino_devices():
        """Intelligently load capsules onto available OpenVINO-compatible
        devices.

        Since support for OpenVINO devices is experimental, there is a
        temporary environment variable being added to whitelist devices
        specifically. This variable will be deprecated and removed after a
        short testing period.

        OPENVINO_ALLOWABLE_DEVICES can be
            "", "HDDL", or "MYRIAD"
        The device "CPU" is _always_ allowed and always loaded onto and cannot
        be excluded.

        Here are the cases:
        ['CPU:0', 'MYRIAD', ...] => ["MULTI:CPU,MYRIAD.1,MYRIAD.2,..."]
            If MYRIAD is whitelisted. Else, it will return ["CPU"]
        ['CPU:0', 'HDDL', ...] =>  ["MULTI:CPU,HDDL"]
            If HDDL is whitelisted. Else, it will return ["CPU"]
        ['CPU:0'] => ["CPU"]
            Always load onto CPU.
        """

        def filter_func(devices):
            allowed_device_type = os.environ.get(
                "OPENVINO_ALLOWABLE_DEVICES", None)

            allowed_devices = []
            if allowed_device_type in (None, ""):
                logging.info("No devices specified in "
                             "OPENVINO_ALLOWABLE_DEVICES. Loading onto CPU.")
            elif allowed_device_type.lower() in ("myriad", "hddl"):
                allowed_devices = [
                    d for d in devices
                    if d.lower().startswith(allowed_device_type.lower())]
                if not len(allowed_devices):
                    logging.warning("OPENVINO_ALLOWABLE_DEVICES specified "
                                    f"{allowed_device_type}, but no such "
                                    f"device was found.")
            else:
                logging.warning(
                    "Invalid value for OPENVINO_ALLOWABLE_DEVICES. "
                    f"Loading onto CPU only. Value: '{allowed_device_type}'")

            devices = ["CPU"] + allowed_devices

            if len(allowed_devices):
                return ["MULTI:" + ",".join(devices)]
            else:
                return devices

        return DeviceMapper(filter_func=filter_func)
