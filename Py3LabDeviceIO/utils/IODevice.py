import os
import signal


class IODevice:
    def __init__(self, path_to_device):
        self.device = path_to_device
        self.file_descriptor = os.open(path_to_device, os.O_RDWR | os.O_NOCTTY)

    def write(self, command):
        os.write(self.file_descriptor, command.encode())

    def read(self, length=4000):
        return os.read(self.file_descriptor, length)

    def close(self):
        os.close(self.file_descriptor)

    def get_name(self):
        self.write("*IDN?")
        return self.read(300)

    def read_error(self):
        self.write("SYSTem:ERRor?")
        msg_error = self.read(100)
        return msg_error

    def clear_event_register(self):
        self.write("*CLS")

    def handler(self, signum, frame):
        pass

    def __del__(self):
        self.close()