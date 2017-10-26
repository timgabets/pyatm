def parce_trace_data(data):
  parsed = ''
  if data: 
    splitted = data.split('|')
    for trace_string in splitted:
      if trace_string[0] == ' ':
        i = 0
        while i < 16:
          parsed += bytes('\\x' + trace_string[3*i+1 : 3*i+3], 'utf-8')
          i += 1

  return parsed
