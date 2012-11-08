#!/usr/bin/env python

import serial
import threading

class SerialReceiver(threading.Thread):
    def __init__(self, device, *args):
        self._target = self.read
        self._args = args

        self.ser = serial.Serial(device)  # open first serial port
        print self.ser.portstr       # check which port was really used
        self.data_buffer = ""

        self.closing = False

        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)

    def read(self):
        while not self.closing:
            self.data_buffer += self.ser.read(6)
        self.ser.close()

    def pop_buffer(self):
        buf = self.data_buffer
        self.data_buffer = ""
        return buf

    def write(data):
        self.ser.write(data)

    def close(self):
        self.closing = True


if __name__ == "__main__":
    device = '/dev/tty.usbserial'
    s1 = SerialReceiver(device)
    s1.start()

    try:
        while True:
            data = s1.pop_buffer()
            if data != "": print repr(data)
    except KeyboardInterrupt:
        s1.close()
    finally:
        s1.close()
    s1.join()