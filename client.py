#!/usr/bin/env python3

import socket
import sys
from datetime import datetime

s = socket.socket()
port = 5000
ip = '127.0.0.1'
try:
    s.connect((ip, port))
except Exception as e:
    print('Exception occured:', str(e))
    quit()
print('Connected to server on ', ip, ':', port)
print('Type \'quit\' to exit')
while True:
    inp = input('Enter request ')
    file = (inp.split())
    if len(file) < 2 and inp != 'quit':
        print('Incorrect format')
        continue
    if (inp == 'quit'):
        s.send(str.encode(inp))
        s.close()
        break
    if file[0] != 'GET':
        print('Incorrect format')
        continue
    s.send(str.encode(file[1]))
    status = (s.recv(4096)).decode('utf-8')
    if (status != 'OK'):
        print('File not found')
        continue
    fName = file[1].split('/')
    fName = fName[len(fName) - 1]
    f = open(fName, 'wb')
    while True:
        data = s.recv(4096)
        while len(data) != 0:
            f.write(data)
            if len(data) < 4096:
                break
            data = s.recv(4096)
        f.close()
        break
    print('File', fName, 'written')
