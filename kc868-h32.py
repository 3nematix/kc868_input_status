"""
    This code is to calculate input statuses for KC868-H32 Device.
    Made by: 3nematix (github)
"""

import os
import socket
import time

edsIP = "192.168.11.3"  # IP address of your KC868-H32 device.
edsPORT = 4196  # PORT of your device.

STATE_INPUT = "RELAY-GET_INPUT-255"

current_ses = 0  # Create a little tracking system.

limited_calculations = False  # You can set a rate limitation for calculations.
limited_rate = 10  # If limited_calculations is set to True, you need to set a value.

while True:
    try:
        current_ses += 1
        os.system('clear')

        # Limited rate of calculations available.
        if limited_calculations is True:
            if current_ses > limited_rate:
                print('Calculations have been completed, stopping the client.')
                break

        # Connect to the device through socket.

        srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srvsock.settimeout(3)
        srvsock.connect((edsIP, edsPORT))
        srvsock.sendto(STATE_INPUT.encode(), (edsIP, edsPORT))
        data = srvsock.recv(4096).decode('utf-8')

        # Replace the tags that we don't need for our further actions.
        data1 = data.replace('RELAY-GET_INPUT-255,', '')
        data2 = data1.replace(',OK', '')
        decimal_num = data2.rstrip('\x00')

        # Convert a decimal number into a binary.
        binary = bin(int(decimal_num))[4:]  # We have 6 inputs in our device, so we need only 6 digits of binary.

        # Input status: 1 - OFF, 0 - ON. ( Binary )

        print(f'Session {current_ses} details:\nDecimal num received - {decimal_num}\nBinary converted - {binary}')

        print('Input 1 is OFF') if binary[5] == '1' else print('Input 1 is ON')
        print('Input 2 is OFF') if binary[4] == '1' else print('Input 2 is ON')
        print('Input 3 is OFF') if binary[3] == '1' else print('Input 3 is ON')
        print('Input 4 is OFF') if binary[2] == '1' else print('Input 4 is ON')
        print('Input 5 is OFF') if binary[1] == '1' else print('Input 5 is ON')
        print('Input 6 is OFF') if binary[0] == '1' else print('Input 6 is ON')

    except Exception as er:
        print(er)
        continue

    finally:
        srvsock.close()  # Stop the Client.
        time.sleep(3)  # Delay after re-starting calculations.
