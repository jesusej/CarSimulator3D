# Created by Youssef Elashry to allow two-way communication between Python3 and Unity to send and receive strings

# Feel free to use this in your individual or commercial projects BUT make sure to reference me as: Two-way communication between Python 3 and Unity (C#) - Y. T. Elashry
# It would be appreciated if you send me how you have used this in your projects (e.g. Machine Learning) at youssef.elashry@gmail.com

# Use at your own risk
# Use under the Apache License 2.0

# Example of a Python UDP server

import UdpComms as U
import time
import json

# Create UDP socket to use for sending (and receiving)
sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)

i = 0

while True:
    jsonObject = {"Cars":[
        {
            "CarId":76,
            "Position":{
                "x":10,
                "y":20,
                "z":30
            }
        },
        {
            "CarId":332,
            "Position":{
                "x":44,
                "y":55,
                "z":66
            }
        }
    ]}
    jsonData = json.dumps(jsonObject)
    sock.SendJsonData(jsonData.encode()) # Send this string to other application str(i)
    i += 1

    data = sock.ReadReceivedData() # read data

    if data != None: # if NEW data has been received since last ReadReceivedData function call
        print(data) # print new received data

    time.sleep(1)