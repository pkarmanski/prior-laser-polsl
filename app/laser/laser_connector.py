import time

import serial


class LaserConnector:
    def __init__(self, com_port):
        self.__com_port = com_port
        self.__baudrate = 115200
        self.__timeout = 0.1
        self.__laser = serial.Serial(self.__com_port, self.__baudrate, timeout=self.__timeout)

    def set_com_port(self, com_port: str):
        self.__com_port = com_port
        print(self.__com_port)

    def write_data(self, value):
        self.__laser.write(bytes(value, 'utf-8'))
        time.sleep(0.1)
        print(self.__laser.readline())
