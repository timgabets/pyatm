import unittest

from pyatm.tools import parce_trace_data, is_atm_message, is_start_of_atm_message, is_host_message_sent, get_timestamp

class TestParseTraceData(unittest.TestCase):
  def test_parce_trace_data(self):
    self.assertEqual(parce_trace_data(''), b'')

  def test_parce_trace_single_string_data(self):
    data = """13:51:42.580796 -| 31.31.1C.30.30.35.30.30.30.30.30.30.1C.1C.1C.31       11.005000000...1"""
    self.assertEqual(parce_trace_data(data), b'11\x1c005000000\x1c\x1c\x1c1')

  def test_parce_trace_line_2(self):
    data = """13:51:42.580806 -| 31.1C.3B.36.30.33.37.39.39.31.30.31.32.33.34.35       1.;6037991012345"""
    self.assertEqual(parce_trace_data(data), b'1\x1c;6037991012345')

  def test_parce_trace_line_3(self):
    data = """13:51:42.580815 -| 36.37.34.3D.32.30.30.33.31.30.31.31.32.39.35.37       674=200310112957"""
    self.assertEqual(parce_trace_data(data), b'674=200310112957')

  def test_parce_trace_line_4(self):
    data = """13:51:42.580824 -| 34.30.37.3F.1C.1C.46.49.20.20.49.20.20.41.1C.30       407?..FI  I  A.0"""
    self.assertEqual(parce_trace_data(data), b'407?\x1c\x1cFI  I  A\x1c0')

  def test_parce_trace_line_5(self):
    data = """13:51:42.580833 -| 30.30.30.30.30.30.30.1C.31.3A.39.30.3F.3D.3F.30       0000000.1:90?=?0"""
    self.assertEqual(parce_trace_data(data), b'0000000\x1c1:90?=?0')      

  def test_parce_trace_line_6(self):
    data = """13:51:42.580842 -| 3F.34.32.30.35.34.34.36.1C.1C.1C.1C.32.35.37.31       ?4205446....2571"""
    self.assertEqual(parce_trace_data(data), b'?4205446\x1c\x1c\x1c\x1c2571')      

  def test_parce_trace_line_7(self):
    data = """13:51:42.580851 -| 36.31.30.30.30.30.30.30.30.30.30.30.30.30.30.30       6100000000000000"""
    self.assertEqual(parce_trace_data(data), b'6100000000000000')      

  def test_parce_trace_line_8(self):
    data = """13:51:42.580858 -| 30.30.30.30.30.30                                     000000  """
    self.assertEqual(parce_trace_data(data), b'000000')

  def test_parce_trace_transaction_request(self):
    data = """13:51:42.580796 -| 31.31.1C.30.30.35.30.30.30.30.30.30.1C.1C.1C.31       11.005000000...1
    13:51:42.580806 -| 31.1C.3B.36.30.33.37.39.39.31.30.31.32.33.34.35       1.;6037991012345
    13:51:42.580815 -| 36.37.34.3D.32.30.30.33.31.30.31.31.32.39.35.37       674=200310112957
    13:51:42.580824 -| 34.30.37.3F.1C.1C.46.49.20.20.49.20.20.41.1C.30       407?..FI  I  A.0
    13:51:42.580833 -| 30.30.30.30.30.30.30.1C.31.3A.39.30.3F.3D.3F.30       0000000.1:90?=?0
    13:51:42.580842 -| 3F.34.32.30.35.34.34.36.1C.1C.1C.1C.32.35.37.31       ?4205446....2571
    13:51:42.580851 -| 36.31.30.30.30.30.30.30.30.30.30.30.30.30.30.30       6100000000000000
    13:51:42.580858 -| 30.30.30.30.30.30                                     000000  """
    self.assertEqual(parce_trace_data(data), b'11\x1c005000000\x1c\x1c\x1c11\x1c;6037991012345674=200310112957407?\x1c\x1cFI  I  A\x1c00000000\x1c1:90?=?0?4205446\x1c\x1c\x1c\x1c25716100000000000000000000')


class testIsStartOfATMMessage(unittest.TestCase):
  def test_is_strart_of_atm_message_empty_data(self):
    self.assertEqual(is_start_of_atm_message(''), False)

  def test_is_start_of_atm_message_valid_data(self):
    self.assertEqual(is_start_of_atm_message("""13:51:42.580796 -| 31.31.1C.30.30.35.30.30.30.30.30.30.1C.1C.1C.31       11.005000000...1"""), True)
    self.assertEqual(is_start_of_atm_message("""13:51:42.580806 -| 31.1C.3B.36.30.33.37.39.39.31.30.31.32.33.34.35       1.;6037991012345"""), False)


class TestIsATMMessage(unittest.TestCase):
  def test_is_atm_message_empty_data(self):
    self.assertEqual(is_atm_message(''), False)

  def test_is_atm_message_valid_data(self):
    self.assertEqual(is_atm_message("""13:51:42.580796 -| 31.31.1C.30.30.35.30.30.30.30.30.30.1C.1C.1C.31       11.005000000...1"""), True)
    self.assertEqual(is_atm_message("""13:51:42.580806 -| 31.1C.3B.36.30.33.37.39.39.31.30.31.32.33.34.35       1.;6037991012345"""), True)
    self.assertEqual(is_atm_message("""13:51:42.580815 -| 36.37.34.3D.32.30.30.33.31.30.31.31.32.39.35.37       674=200310112957"""), True)
    self.assertEqual(is_atm_message("""13:51:42.580824 -| 34.30.37.3F.1C.1C.46.49.20.20.49.20.20.41.1C.30       407?..FI  I  A.0"""), True)
    self.assertEqual(is_atm_message("""13:51:42.580833 -| 30.30.30.30.30.30.30.1C.31.3A.39.30.3F.3D.3F.30       0000000.1:90?=?0"""), True)
    self.assertEqual(is_atm_message("""13:51:42.580842 -| 3F.34.32.30.35.34.34.36.1C.1C.1C.1C.32.35.37.31       ?4205446....2571"""), True)
    self.assertEqual(is_atm_message("""13:51:42.580851 -| 36.31.30.30.30.30.30.30.30.30.30.30.30.30.30.30       6100000000000000"""), True)
    self.assertEqual(is_atm_message("""13:51:42.580858 -| 30.30.30.30.30.30                                     000000"""), True)
    self.assertEqual(is_atm_message("""13:51:42.580858 -| 30                                                    0"""), True)
    self.assertEqual(is_atm_message("""16:51:15.950531 -| E8.03.00.00.00.00.00.00.00.FF.FF.FF.89.B2.01.00       ................"""), True)

  def test_is_atm_message_invalid_data(self):
    self.assertEqual(is_atm_message("""16:51:29.803538 -| constructed buffer string"""), False)


class TestIsHostMessageSent(unittest.TestCase):
  def test_is_host_message_sent_empty_data(self):
    self.assertEqual(is_host_message_sent(''), False)  

  def test_is_atm_message_invalid_data(self):
    self.assertEqual(is_host_message_sent("""13:51:42.580796 -| 31.31.1C.30.30.35.30.30.30.30.30.30.1C.1C.1C.31       11.005000000...1"""), False)
    self.assertEqual(is_host_message_sent("""14:35:39.910408 -| msgsnd_w_retry [dst task: COMMSINT, time: 31/10/2017 14:35:39.910]: trying to send 253d bytes to target queue 76775432"""), False)

  
  def test_is_atm_message_valid_data(self):
    self.assertEqual(is_host_message_sent("""14:35:39.910431 D| msgsnd_w_retry [dst task: COMMSINT, time: 31/10/2017 14:35:39.910]: Send msg to queue 76775432"""), True)


class testGetTimestamp(unittest.TestCase):
  def test_get_timestamp_empty_data(self):
    self.assertEqual(get_timestamp(''), None)    

  def test_get_timestamp_nonempty_data(self):
    self.assertEqual(get_timestamp("""14:35:39.910431 D| <- only this format is currently supported"""), "14:35:39.910431")
    self.assertEqual(get_timestamp("""14:35:39 | <- this format is not supported"""), None)
    self.assertEqual(get_timestamp("""iddqd"""), None)

if __name__ == '__main__':
  unittest.main()