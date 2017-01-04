import argparse
import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import time
base_dir_path = ("/".join(os.getcwd().split("/")[:-1]))
path_to_Py3LabDeviceIO = os.path.join(base_dir_path, "Py3LabDeviceIO")
path_to_utils = os.path.join(base_dir_path, "Py3LabDeviceIO", "utils")
sys.path.insert(0, path_to_Py3LabDeviceIO)
sys.path.insert(0, path_to_utils)


from device import Device


def do_measure(numbers_of_point_to_measure, start_current, stop_current, output_file):
    try:
        dev = Device()
        ldc4005 = dev.get_ldc4005_instance()
        pm100 = dev.get_pm100_instance()
    except Exception as err:
        print("Proble in connect with device")
        sys.exit(1)

    current = np.linspace(float(start_current)*1e-3, float(stop_current)*1e-3, numbers_of_point_to_measure)
    voltage = np.zeros(numbers_of_point_to_measure)
    power = np.zeros(numbers_of_point_to_measure)
    try:
        ldc4005.on()
        time.sleep(1)
        for i in range(0, numbers_of_point_to_measure):
            ldc4005.set_ld_current_in_amper(current[i])
            time.sleep(0.1)
            current[i] = ldc4005.ld_current_reading()
            voltage[i] = ldc4005.ld_voltage_reading()
            power[i] = pm100.get_power()
    except Exception as err:
        print(err)
    finally:
        ldc4005.off()

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(current*1000, power*1000, marker='o', color='red', ls='none')
    ax2.plot(current*1000, voltage, marker='o', color='green', ls='none')

    ax1.set_xlabel('Current [mA]')
    ax1.set_ylabel('Power [mW]', color='r')
    ax2.set_ylabel('Voltage [V]', color='g')
    save_data(output_file, current, voltage, power)
    plt.grid(True)
    plt.show()


def save_data(output_file, current, voltage, power):
    now = datetime.datetime.now()
    info = "Measurment \n"
    info += now.strftime("%Y-%m-%d %H:%M")
    np.savetxt(output_file, np.c_[current, voltage, power], fmt='%1.16f', header=info)


if __name__ == "__main__":
    CURRENT_WORKING_DIRECTORY = os.getcwd()
    OUTPUT_FILE = os.path.join(CURRENT_WORKING_DIRECTORY, "output")

    parser = argparse.ArgumentParser(description='Give parameters to measure IVL laser diode.')
    parser.add_argument("-nr", "--numbers_of_points_to_measure", type=int,
                    default=0, help='Numbers of points to measure')
    parser.add_argument("-sc", "--start_current", type=float,
                    default=0, help="Start current in mA")
    parser.add_argument("-ec", "--stop_current", type=float,
                    default=0, help="Stop current in mA")
    parser.add_argument("-fn", "--file_name", type=str,
                    default=os.path.join(OUTPUT_FILE, "data.txt"),
                    help="path to output file")

    args = parser.parse_args()
    print("Numbers of points to measure: %s"  %args.numbers_of_points_to_measure)
    print("Start current %s mA" %args.start_current)
    print("Stop current %s mA"  %args.stop_current)
    print("Path to output file with data:", end=" ")
    print(args.file_name)

    do_measure(args.numbers_of_points_to_measure, args.start_current, args.stop_current, args.file_name)
