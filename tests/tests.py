import unittest

from pyatm.tools import parce_trace_data


class TestParseTraceData(unittest.TestCase):
    def test_parce_trace_data(self):
        self.assertEqual(parce_trace_data(''), b'')

if __name__ == '__main__':
  unittest.main()