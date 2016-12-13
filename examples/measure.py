import os
import sys
base_dir_path = ("/".join(os.getcwd().split("/")[:-1]))
path_to_Py3LabDeviceIO = os.path.join(base_dir_path, "Py3LabDeviceIO")
path_to_utils = os.path.join(base_dir_path, "Py3LabDeviceIO", "utils")
sys.path.insert(0, path_to_Py3LabDeviceIO)
sys.path.insert(0, path_to_utils)

from device import Device

dev = Device()
dev.available_device()

