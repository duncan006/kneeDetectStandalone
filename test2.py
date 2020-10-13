#!/usr/bin/env python3

from serialSend import *
import serial

teensyPort = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=3.0)

while True:
    dataReceived, teensyArray = receive_from_teensy(teensyPort)
    if dataReceived:
        torqueL = teensyArray[0]
        torqueR = teensyArray[1]
        send_to_teensy(2345, 4567, teensyPort)
