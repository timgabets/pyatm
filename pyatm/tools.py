import binascii
import re

def parce_trace_data(data):
  parsed = b''
  if data: 
    splitted = data.split('|')
    for trace_string in splitted:
      if trace_string[0] == ' ':
        i = 0
        while i < 16:
          try:
            parsed += binascii.unhexlify(trace_string[3*i+1 : 3*i+3])
          except binascii.Error:
            break
          i += 1          
  return parsed


def is_start_of_atm_message(trace_line):
  """
  Detects whether the provided line looks like the beginning of the ATM message
  """
  if re.match("^\d{2}:\d{2}:\d{2}.\d{6} -\| (3[1-2]\.){2}1C.*[ ]{7}[1-2]{2}", trace_line):
    return True

  return False


def is_atm_message(trace_line):
  """
  Detects whether the provided line is ATM message from trace file.
  """
  if re.match("^\d{2}:\d{2}:\d{2}.\d{6} -\| [0-9A-F]{2}.*[ ]{7}.", trace_line):
    return True
  
  return False


def is_host_message_sent(trace_line):
  """
  Detects whether the provided line looks like 
  14:35:39.910431 D| msgsnd_w_retry [dst task: COMMSINT, time: 31/10/2017 14:35:39.910]: Send msg to queue 76775432
  """

  if re.match("^\d{2}:\d{2}:\d{2}.\d{6} .\| msgsnd_w_retry \[dst task: COMMSINT, time: \d{2}\/\d{2}\/\d{4} \d{2}:\d{2}:\d{2}.\d{3}]: Send msg to queue", trace_line):
    return True

  return False


def get_timestamp(line):
  """
  returns the timestamp
  """
  if line and re.match("^\d{2}:\d{2}:\d{2}.\d{6}", line):
    return line[0:15]

  return None
