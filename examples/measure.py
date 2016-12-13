import argparse
import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
base_dir_path = ("/".join(os.getcwd().split("/")[:-1]))
path_to_Py3LabDeviceIO = os.path.join(base_dir_path, "Py3LabDeviceIO")
path_to_utils = os.path.join(base_dir_path, "Py3LabDeviceIO", "utils")
sys.path.insert(0, path_to_Py3LabDeviceIO)
sys.path.insert(0, path_to_utils)


from device import Device


def do_measure(numbers_of_point_to_measure, start_current, stop_current, output_file):
    current = np.zeros(numbers_of_point_to_measure)
    voltage = np.zeros(numbers_of_point_to_measure)
    power = np.zeros(numbers_of_point_to_measure)
    for i in range(0, numbers_of_point_to_measure):
        current[i] = i
        voltage[i] = i*i
        power[i] = 2*i

    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    ax1.plot(current, power, marker='o', color='red', ls='none')
    ax2.plot(current, voltage, marker='o', color='green', ls='none')

    ax1.set_xlabel('J [A]')
    ax1.set_ylabel('L [W]', color='r')
    ax2.set_ylabel('U [V]', color='g')
    save_data(output_file, current, voltage, power)
    plt.grid(True)
    plt.show()


def save_data(output_file, current, voltage, power):
    now = datetime.datetime.now()
    info = "Measurment \n"
    info += now.strftime("%Y-%m-%d %H:%M")
    np.savetxt(output_file, np.c_[current, voltage, power], fmt='%1.16f', header=info)

CURRENT_WORKING_DIRECTORY = os.getcwd()
OUTPUT_FILE = os.path.join(CURRENT_WORKING_DIRECTORY, "output")

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("-nr", "--numbers_of_points_to_measure", type=int,
                    default=0, help='Numbers of points to measure')
parser.add_argument("-sc", "--start_current", type=float,
                    default=0, help="Start current")
parser.add_argument("-ec", "--stop_current", type=float,
                    default=0, help="Stop current")
parser.add_argument("-fn", "--file_name", type=str,
                    default=os.path.join(OUTPUT_FILE, "data.txt"),
                    help="path to output directory")


args = parser.parse_args()
print(args.numbers_of_points_to_measure)
print(args.file_name)


dev = Device()
dev.available_device()


do_measure(args.numbers_of_points_to_measure, args.start_current, args.stop_current, args.file_name)