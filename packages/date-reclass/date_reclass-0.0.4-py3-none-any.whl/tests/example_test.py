import unittest
import pprint
# from ..main.crawls.models import Crawls

p = pprint.PrettyPrinter(indent=4)

class ExampleTest(unittest.TestCase):
  def test_example(self):
    results = 5
    self.assertEqual(results, 5)