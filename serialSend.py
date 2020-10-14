def receive_from_teensy(serialPort):
    import struct
    receivedData = False
    outputArray = []
    
    firstChar = serialPort.read() #Byte 1
    
    if (firstChar == b'\xa5'):
        secondChar = serialPort.read() #Byte 2
        if (secondChar == b'\x5a'):
            dataSize = serialPort.read() #Byte 3
            dataSizeInt = struct.unpack('B',dataSize)
            
            LTorqueLO = serialPort.read() #Byte 4
            LTorqueHI = serialPort.read() #Byte 5
            LTorque = struct.unpack('<H', LTorqueHI + LTorqueLO)
            
            RTorqueLO = serialPort.read() #Byte 6
            RTorqueHI = serialPort.read() #Byte 7
            RTorque = struct.unpack('<H', RTorqueHI + RTorqueLO)
            
            LKneeAngleLO = serialPort.read() #Byte 8
            LKneeAngleHI = serialPort.read() #Byte 9
            LKneeAngle = struct.unpack('<H', LKneeAngleHI + LKneeAngleLO)
            
            RKneeAngleLO = serialPort.read() #Byte 10
            RKneeAngleHI = serialPort.read() #Byte 11
            RKneeAngle = struct.unpack('<H', RKneeAngleHI + RKneeAngleLO)
            
            LTAngleLO = serialPort.read() #Byte 12
            LTAngleHI = serialPort.read() #Byte 13
            LTAngle = struct.unpack('<H', LTAngleHI + LTAngleLO)
            
            RTAngleLO = serialPort.read() #Byte 14
            RTAngleHI = serialPort.read() #Byte 15
            RTAngle = struct.unpack('<H', RTAngleHI + RTAngleLO)
            
            LSAngleLO = serialPort.read() #Byte 16
            LSAngleHI = serialPort.read() #Byte 17
            LSAngle = struct.unpack('<H', LSAngleHI + LSAngleLO)
            
            RSAngleLO = serialPort.read() #Byte 18
            RSAngleHI = serialPort.read() #Byte 19
            RSAngle = struct.unpack('<H', RSAngleHI + RSAngleLO)
            
            LTangVLO = serialPort.read() #Byte 20
            LTangVHI = serialPort.read() #Byte 21
            LTangV = struct.unpack('<H', LTangVHI + LTangVLO)
            
            RTangVLO = serialPort.read() #Byte 22
            RTangVHI = serialPort.read() #Byte 23
            RTangV = struct.unpack('<H', RTangVHI + RTangVLO)
            
            LSangVLO = serialPort.read() #Byte 24
            LSangVHI = serialPort.read() #Byte 25
            LSangV = struct.unpack('<H', LSangVHI + LSangVLO)
            
            RSangVLO = serialPort.read() #Byte 26
            RSangVHI = serialPort.read() #Byte 27
            RSangV = struct.unpack('<H', RSangVHI + RSangVLO)
            
            outputArray = [LTorque[0], RTorque[0], LKneeAngle[0], RKneeAngle[0], LTAngle[0], RTAngle[0], LSAngle[0], RSAngle[0], LTangV[0], RTangV[0], LSangV[0], RSangV[0]]
            receivedData = True
            print(outputArray)
    
    return receivedData, outputArray
    
def send_to_teensy(torqueLeft, torqueRight, serialPort):
    import struct
    import serial
    import time
    
    #Bytes (7 total):
    #0: 165
    #1: 90
    #2: data length (4 bytes)
    #3: left torque high byte
    #4: left torque low byte
    #5: right torque high byte
    #6: right torque low byte
    
    sendStr = bytearray(struct.pack("B", 165))
    sendStr += bytearray(struct.pack("B", 90))
    sendStr += bytearray(struct.pack("B", 52))
    sendStr += bytearray(struct.pack("<H", int(torqueLeft * 1000)))
    sendStr += bytearray(struct.pack("<H", int(torqueRight * 1000)))
    print(sendStr)
    serialPort.write(sendStr)
