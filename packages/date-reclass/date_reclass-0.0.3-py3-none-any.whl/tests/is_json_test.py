import unittest
import json
from date_reclass import is_json

class IsJsonTest(unittest.TestCase):
  def test_is_json(self):
    results = is_json(json.dumps("{'foo': 'bar'}"))
    self.assertEqual(results, True)

    results = is_json(json.dumps("[{'foo': 'bar'}]"))
    self.assertEqual(results, True)

  def test_is_not_json(self):
    results = is_json("{'foo': 'bar'}")
    self.assertEqual(results, False)
    
    results = is_json("[{'foo': 'bar'}]")
    self.assertEqual(results, False)