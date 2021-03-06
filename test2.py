#!/usr/bin/env python3

from serialSend import *
import serial

teensyPort = serial.Serial("/dev/ttyS0", baudrate=256000, timeout=3.0)

while True:
    dataReceived, teensyArray = receive_from_teensy(teensyPort)
    if dataReceived:
        torqueL = teensyArray[0]
        torqueR = teensyArray[1]
        send_to_teensy(torqueL/1000, torqueR/1000, teensyPort)
