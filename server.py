#!/usr/bin/env python3

import os
import socket
import mimetypes
from _thread import *


def startListen():
    while True:
        c, a = s.accept()
        print('Client', a[0], ':', a[1], 'connected')
        start_new_thread(sendFileCLI, (c, a))
    s.close()


def sendBinaryData(text, conn):
    with open(text, 'rb') as f:
        packet = f.read(4096)
        while len(packet) != 0:
            conn.send(packet)
            packet = f.read(4096)


def sendFileCLI(conn, addr):
    while True:
        text = conn.recv(4096)
        text = text.decode('utf-8')
        if not text:
            break
        print(addr[0], ':', addr[1], 'said', text)
        if text == 'quit':
            break
        if 'favicon' in text:
            print('Ignoring favicon.ico request')
            break
        if len(text.split('\n')) > 1:
            sendFileBrowser(conn, addr, text.split('\n')[0])
            break
        if not os.path.exists(text):
            conn.send(str.encode('File not found'))
            continue
        conn.send(str.encode('OK'))
        try:
            sendBinaryData(text, conn)
            print('File transferred to', addr[0], ':', addr[1])
        except Exception as e:
            print('Exception occured:', str(e))
    conn.close()
    print(addr[0], ':', addr[1], 'disconnected')


def sendFileBrowser(conn, addr, data):
    text = data.split()[1]
    if text[0] == '/':
        text = text.replace('/', '', 1)
    if not os.path.exists(text):
        conn.send(
            str.encode(
                'HTTP/1.1 404 Not Found\nContent-Type: text/plain; charset=utf-8\n\nFile not found'
            ))
        conn.close()
        print('File', text, 'not found')
        print(addr[0], ':', addr[1], 'disconnected')
        return
    content_type = mimetypes.MimeTypes().guess_type(text)[0]
    headers = f'HTTP/1.1 200 OK\nContent-Type: {content_type}\n\n'
    conn.send(str.encode(headers))
    try:
        sendBinaryData(text, conn)
        print('File transferred to', addr[0], ':', addr[1])
    except Exception as e:
        print('Exception occured:', str(e))
    conn.close()
    print(addr[0], ':', addr[1], 'disconnected')


port = 5000
ip = '127.0.0.1'
s = socket.socket()
try:
    s.bind((ip, port))
except Exception as e:
    print('Exception occured:', str(e))

s.listen(5)  #max queued clients=5
print('Server running on http://' + ip + ':' + str(port))
print('HIT ENTER TO EXIT')
start_new_thread(startListen, ())
input()