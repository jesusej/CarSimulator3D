import socket
import random
import json
from time import sleep

def RandomPosition():
    s = socket.socket()
    jsonResult = {"first":"You're", "second":"Awsome!", "alan":10}
    jsonResult = json.dumps(jsonResult)
              
    # connect to the server on local computer 
    s.connect(('192.168.0.4', 3000))
    s.send(jsonResult.encode())
    """s.send((
        str(random.uniform(0, 1)) + ","+
        str(random.uniform(0, 1)) + ","+
        str(random.uniform(0, 1))).encode())
    s.close()"""

for i in range(500):
    RandomPosition()
    sleep(1)
