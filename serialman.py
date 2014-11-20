#!/usr/bin/env python

import serial
import threading
import time
from multiprocessing import Process, Queue
try:
    from queue import Empty
except:
    from Queue import Empty

class SerialManager(Process):
    """ This class has been written by
        Philipp Klaus and can be found on
        https://gist.github.com/4039175 .  """
    def __init__(self, device, **kwargs):
        settings = dict()
        settings['baudrate'] = 9600
        settings['bytesize'] = serial.EIGHTBITS
        settings['parity'] = serial.PARITY_NONE
        settings['stopbits'] = serial.STOPBITS_ONE
        settings['timeout'] = 0
        settings.update(kwargs)
        self._kwargs = settings
        self.ser = serial.Serial(device, **self._kwargs)
        self.in_queue = Queue()
        self.out_queue = Queue()
        self.closing = False # A flag to indicate thread shutdown
        self.sleeptime = 0.0005
        Process.__init__(self, target=self.loop)

    def loop(self):
        try:
            while not self.closing:
                time.sleep(self.sleeptime)
                in_data = self.ser.read(256)
                if in_data: self.in_queue.put(in_data)
                try:
                    out_buffer = self.out_queue.get_nowait()
                    self.ser.write(out_buffer)
                except Empty:
                    pass
        except (KeyboardInterrupt, SystemExit):
            pass
        self.ser.close()

    def close(self):
        self.closing = True

def main():
    import argparse
    parser = argparse.ArgumentParser(description='A class to manage reading and writing from and to a serial port.')
    parser.add_argument('--sleeptime', '-s', type=float, default=0.001, help='Seconds to sleep between polling (0.001s).')
    parser.add_argument('--baudrate', '-b', type=int, default=9600, help='Baudrate of serial port.')
    parser.add_argument('device', help='The serial port to use (COM4, /dev/ttyUSB1 or similar).')
    args = parser.parse_args()

    s1 = SerialManager(args.device, baudrate=args.baudrate)
    s1.sleeptime = args.sleeptime
    s1.start()

    try:
        while True:
            data = s1.in_queue.get()
            print(repr(data))
    except KeyboardInterrupt:
        s1.close()
    finally:
        s1.close()
    s1.join()

if __name__ == "__main__":
    main()

