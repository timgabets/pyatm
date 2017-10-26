#!/usr/bin/env python

import socket
import struct
import sys

from tools import parce_trace_data
from tracetools.tracetools import trace

class ATM:
  def __init__(self, host, port):
    """
    """
    self.host = host
    self.port = port

    try:
        self.sock = None
        for res in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            self.sock = socket.socket(af, socktype, proto)
            self.sock.connect(sa)
    except OSError as msg:
        print('Error connecting to {}:{} - {}'.format(self.host, self.port, msg))
        sys.exit()

    print('Connected to {}:{}'.format(self.host, self.port))


  def get_message_length(self, message):
    """
    """
    return b'\x00\x00'


  def send(self, data):
    """
    """
    data = struct.pack("!H", len(data)) + data
    self.sock.send(data)
    trace('>> {} bytes sent:'.format(len(data)), data)


  def recv(self):
    """
    """
    data = self.sock.recv(4096)    
    trace('<< {} bytes received: '.format(len(data)), data)
    return data


if __name__ == '__main__':
  atm = ATM('127.0.0.1', 11032)
  
  data = """18:15:07.976484 -| 31.31.1C.30.30.35.30.30.30.30.30.30.1C.1C.1C.31       11.005000000...1
  18:15:07.976494 -| 35.1C.3B.36.30.33.37.39.39.31.30.31.32.33.34.35       5.;6037991012345
  18:15:07.976502 -| 36.37.34.3D.32.30.30.33.31.30.31.31.32.39.35.37       674=200310112957
  18:15:07.976511 -| 34.30.37.3F.1C.1C.44.46.20.46.49.20.46.44.1C.30       407?..DF FI FD.0
  18:15:07.976520 -| 30.30.30.30.30.30.30.1C.34.3E.37.3C.3B.33.3C.30       0000000.4>7<;3<0
  18:15:07.976529 -| 38.3F.37.3A.34.32.30.3A.1C.39.35.37.36.30.35.39       8?7:420:.9576059
  18:15:07.976538 -| 34.30.34.31.32.33.30.30.30.30.30.33.36.35.36.30       4041230000036560
  18:15:07.976546 -| 33.39.35.1C.1C.1C.32.35.36.34.36.31.30.30.30.30       395...2564610000
  18:15:07.976555 -| 30.30.30.30.30.30.30.30.30.30.30.30.30.30.30.30       0000000000000000"""
  atm.send(parce_trace_data(data))
  atm.recv()
