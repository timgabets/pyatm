import unittest

from pyatm.tools import parce_trace_data

class TestParseTraceData(unittest.TestCase):
    def test_parce_trace_data(self):
        self.assertEqual(parce_trace_data(''), b'')

    def test_parce_trace_single_string_data(self):
      data = """13:51:42.580796 -| 31.31.1C.30.30.35.30.30.30.30.30.30.1C.1C.1C.31       11.005000000...1"""
      self.assertEqual(parce_trace_data(data), b'11\x1c005000000\x1c\x1c\x1c1')

    def _test_parce_trace_data_transaction_request(self):
      data = """13:51:42.580796 -| 31.31.1C.30.30.35.30.30.30.30.30.30.1C.1C.1C.31       11.005000000...1
      13:51:42.580806 -| 31.1C.3B.36.30.33.37.39.39.31.30.31.32.33.34.35       1.;6037991012345
      13:51:42.580815 -| 36.37.34.3D.32.30.30.33.31.30.31.31.32.39.35.37       674=200310112957
      13:51:42.580824 -| 34.30.37.3F.1C.1C.46.49.20.20.49.20.20.41.1C.30       407?..FI  I  A.0
      13:51:42.580833 -| 30.30.30.30.30.30.30.1C.31.3A.39.30.3F.3D.3F.30       0000000.1:90?=?0
      13:51:42.580842 -| 3F.34.32.30.35.34.34.36.1C.1C.1C.1C.32.35.37.31       ?4205446....2571
      13:51:42.580851 -| 36.31.30.30.30.30.30.30.30.30.30.30.30.30.30.30       6100000000000000
      13:51:42.580858 -| 30.30.30.30.30.30                                     000000  """
      self.assertEqual(parce_trace_data(data), b'')

if __name__ == '__main__':
  unittest.main()