from binascii import unhexlify

def parce_trace_data(data):
  parsed = b''
  if data: 
    splitted = data.split('|')
    for trace_string in splitted:
      if trace_string[0] == ' ':
        i = 0
        while i < 16:
          parsed += unhexlify(trace_string[3*i+1 : 3*i+3])
          i += 1

  return parsed
