#!/bin/env python3
"""
Script loads code & other assets onto Raspberry Pi Pico W
"""
__author__ = 'J. B. Otterson'
__copyright__ = 'Copyright 2022, J. B. Otterson N1KDO.'

import os
import pyboard
import serial
import sys
from serial.tools.list_ports import comports
BAUD_RATE = 115200

SRC_DIR = '../temperature/'
FILES_LIST = [
    'content/',
    'data/',
    'main.py',
    'ntp.py',
    'sht30.py',
    'content/files.html',
    'content/temperature.html',
    'content/setup.html',
]


def get_ports_list():
    """
    discover serial ports
    :return: a list of serial port names
    """
    ports = comports()
    ports_list = []
    for port in ports:
        ports_list.append(port.device)
    return sorted(ports_list, key=lambda k: int(k[3:]))


def put_file_progress_callback(bytes_so_far, bytes_total):
    """
    just print a dot
    :param bytes_so_far:
    :param bytes_total:
    :return: None
    """
    print('.', end='')


def put_file(filename, target):
    """
    send a file to a micropython device
    :param filename: the file to send
    :param target: the device to send the file to
    :return: None
    """
    src_file_name = SRC_DIR + filename
    if filename[-1:] == '/':
        filename = filename[:-1]
        try:
            target.fs_mkdir(filename)
            print('created directory {}'.format(filename))
        except Exception as e:
            if 'EEXIST' not in str(e):
                print('failed to create directory {}'.format(filename))
                print(type(e), e)
    else:
        try:
            os.stat(src_file_name)
            print(f'sending file {filename} ', end='')
            target.fs_put(src_file_name, filename, progress_callback=put_file_progress_callback)
            print()
        except OSError as e:
            print(f'cannot find source file {src_file_name}')


def load_device(port):
    target = pyboard.Pyboard(port, BAUD_RATE)
    target.enter_raw_repl()
    for file in FILES_LIST:
        put_file(file, target)
    target.exit_raw_repl()
    target.close()

    # this is a hack that allows the Pico-W to be restarted by this script.
    # it exits the REPL by sending a control-D.
    # why this functionality is not the Pyboard module is a good question.
    with serial.Serial(port=port,
                       baudrate=BAUD_RATE,
                       parity=serial.PARITY_NONE,
                       bytesize=serial.EIGHTBITS,
                       stopbits=serial.STOPBITS_ONE,
                       timeout=1) as pyboard_port:
        pyboard_port.write(b'\x04')
    print('\nDevice should restart.')


def main():
    print('Disconnect the Pico-W if it is connected.')
    input('(press enter to continue...)')
    ports_1 = get_ports_list()
    print(f'Detected serial ports: {" ".join(ports_1)}')
    print('\nConnect the Pico-W to USB port.')
    input('(press enter to continue...)')
    ports_2 = get_ports_list()
    print(f'Detected serial ports: {" ".join(ports_2)}')

    picow_port = None
    for port in ports_2:
        if port not in ports_1:
            picow_port = port
            break

    if picow_port is None:
        print('Could not identify Pico-W communications port.  Exiting.')
        sys.exit(1)

    print(f'\nAttempting to load device on port {picow_port}.')
    load_device(picow_port)


if __name__ == "__main__":
    main()
