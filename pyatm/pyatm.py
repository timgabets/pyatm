#!/usr/bin/env python

import socket
import struct
import sys
import getopt

from time import sleep
from tools import parce_trace_data, is_start_of_atm_message, is_atm_message, is_host_message_sent, get_timestamp
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


def parse_atm_messages(trace_data):
  """
  """
  splitted = trace_data.split('#---+++=== START MESSAGE LOG ===+++---#')

  atm_messages = []
  for chunk in splitted:
    atm_message_found = False
    message = ''

    lines = chunk.split('\n')
    for line in lines:
      if is_start_of_atm_message(line):
        atm_message_found = True
        message += line + '\n'

      elif atm_message_found:
        if is_atm_message(line):
          message += line + '\n'
        else:
          #print(message)
          atm_messages.append(message)
          break
  
  return atm_messages


def parse_host_messages(trace_data):
  lines = trace_data.split('\n')

  host_messages = []
  for line in lines:
    if is_host_message_sent(line):
      host_messages.append(line)

  return host_messages


def parse_trace_file(filename):
  """
  Parse trace file and return requests data
  """
  f = open(filename, 'r')
  trace_data = f.read()

  messages = parse_atm_messages(trace_data) + parse_host_messages(trace_data)
  f.close()
  messages.sort()

  return messages


def show_help(name):
  """

  """
  print('Usage: python3 {} [OPTIONS]... '.format(name))
  print('Dummy ATM message sender')
  print('  -f, --file=[FILE]\t\tatmi.out trace file to parse')
  print('  -s, --start=[timestamp]\t(Optional) send messages starting from this timestamp')
  print('  -e, --end=[timestamp]\t\t(Optional) send messages up to this timestamp')
  

if __name__ == '__main__':
  filename = None
  start_time = None
  end_time = None

  try:
    optlist, args = getopt.getopt(sys.argv[1:], 'h:f:s:e:', ['help', 'file=', 'start=', 'end='])
    for opt, arg in optlist:
      if opt in ('-h', '--help'):
        show_help(sys.argv[0])
        sys.exit()
      
      elif opt in ('-s', '--start'):
        start_time = arg

      elif opt in ('-e', '--end'):
        end_time = arg

      elif opt in ('-f', '--file'):
        filename = arg
    
  except getopt.GetoptError:
    show_help(sys.argv[0])
    sys.exit()

  if not filename:
    show_help(sys.argv[0])
    sys.exit()    

  messages = parse_trace_file(filename)

  atm = ATM('127.0.0.1', 11032)

  for item in messages:
    if start_time and get_timestamp(item) < start_time:
      continue

    if end_time and get_timestamp(item) > end_time:
      break

    if is_host_message_sent(item):
      atm.recv()
    else:
      atm.send(parce_trace_data(item))
