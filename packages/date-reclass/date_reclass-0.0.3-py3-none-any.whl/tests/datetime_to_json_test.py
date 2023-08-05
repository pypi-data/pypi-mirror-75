import unittest
import json
from datetime import datetime
from dateutil.parser import parse
from date_reclass import cast

class DatetimeToJsonTest(unittest.TestCase):
  def test_datetime_to_str(self):
    date = datetime(2020, 5, 17)
    result = cast(date).tostr()
    self.assertEqual(result, '2020-05-17 00:00:00')

  def test_datetime_to_str_formate(self):
    date = datetime(2020, 5, 17)
    result = cast(date, '%d/%m/%y').tostr()
    self.assertEqual(result, '17/05/20')

  def test_datetime_to_str_then_pass_format(self):
    date = datetime(2020, 5, 17)
    jdt = cast(date)
    result = jdt.convert_to_str(format='%d/%m/%y')
    self.assertEqual(result, '17/05/20')

  def test_datetime_to_datatime(self):
    date = '17/05/20'
    result = cast(date).todatetime()
    self.assertEqual(result, datetime(2020, 5, 17, 0, 0))

  def test_str_to_datatime_formatted(self):
    date = '17/05/2020'
    result = cast(date, '%d/%m/%Y').todatetime()
    self.assertEqual(result, datetime(2020, 5, 17, 0, 0))

  def test_str_to_datatime_formatted_then_pass_formatting(self):
    date = '17/05/2020'
    date = cast(date)
    result = date.convert_to_datetime(format='%d/%m/%Y')
    self.assertEqual(result, datetime(2020, 5, 17, 0, 0))

  def test_list_to_datatime(self):
    date = ['17/05/2020','17/05/2021']
    result = cast(date, '%d/%m/%Y').todatetime()
    self.assertEqual(result, [datetime(2020, 5, 17, 0, 0), datetime(2021, 5, 17, 0, 0)])

  def test_dict_to_datatime(self):
    date = {'date1':'17/05/2020','date2':'17/05/2021'}
    result = cast(date, '%d/%m/%Y').todatetime()
    self.assertEqual(result, {'date1': datetime(2020, 5, 17, 0, 0), 'date2': datetime(2021, 5, 17, 0, 0)})

  def test_dict_dict_to_datatime(self):
    date = {'date1':'17/05/2020','date2':{'date2':'17/05/2021'}}
    result = cast(date, '%d/%m/%Y').todatetime()
    self.assertEqual(result, {'date1': datetime(2020, 5, 17, 0, 0), 'date2':{'date2': datetime(2021, 5, 17, 0, 0)}})

  def test_dict_to_datatime_complex(self):
    date = {'date1':'17/05/2020','date2': [{'date2':'17/05/2021'}] }
    result = cast(date, '%d/%m/%Y').todatetime()
    self.assertEqual(result, {'date1': datetime(2020, 5, 17, 0, 0), 'date2':[{'date2': datetime(2021, 5, 17, 0, 0)}] })

  def test_list_list_to_datatime(self):
    date = [['17/05/2020'],  '17/05/2021']
    result = cast(date, '%d/%m/%Y').todatetime()
    self.assertEqual(result, [ [datetime(2020, 5, 17, 0, 0)], datetime(2021, 5, 17, 0, 0)])

  def test_list_to_str(self):
    date = [datetime(2020, 5, 17, 0, 0), datetime(2021, 5, 17, 0, 0)]
    result = cast(date, '%d/%m/%Y').tostr()
    self.assertEqual(result, ['17/05/2020', '17/05/2021'])
  
  def test_list_list_to_str(self):
    date = [datetime(2020, 5, 17, 0, 0), [datetime(2021, 5, 17, 0, 0)]]
    result = cast(date, '%d/%m/%Y').tostr()
    self.assertEqual(result, ['17/05/2020', ['17/05/2021']])

  def test_dict_to_str(self):
    date = {'date1':datetime(2020, 5, 17, 0, 0), 'date2':datetime(2021, 5, 17, 0, 0)}
    result = cast(date, '%d/%m/%Y').tostr()
    self.assertEqual(result, {'date1': '17/05/2020', 'date2': '17/05/2021'})

  def test_dict_dict_to_str(self):
    date = {'date1':datetime(2020, 5, 17, 0, 0),  'date2':{'date2':datetime(2021, 5, 17, 0, 0)}}
    result = cast(date, '%d/%m/%Y').tostr()
    self.assertEqual(result, {'date1': '17/05/2020',  'date2':{'date2': '17/05/2021'}})

  def test_dict_to_str_complex(self):
    date = {'date1':datetime(2020, 5, 17, 0, 0), 'date2': [{'date2':datetime(2021, 5, 17, 0, 0)}] }
    result = cast(date, '%d/%m/%Y').tostr()
    self.assertEqual(result, {'date1': '17/05/2020', 'date2':[{'date2': '17/05/2021'}] })

  def test_str_to_str(self):
    date = '2020-05-17'
    # date = datetime(2020, 5, 17)
    result = cast(date).tostr()
    self.assertEqual(result, '2020-05-17')

  def test_datetime_to_datetime(self):
    date = datetime(2020, 5, 17)
    result = cast(date).todatetime()
    self.assertEqual(result, datetime(2020, 5, 17, 0, 0))

  def test_error_convert_to_formatted_str(self):
    date = datetime(2020, 5, 17)
    # result = cast(date, 1).tostr()
    self.assertRaises(TypeError, cast(date, 1).tostr())

  def test_error_convert_to_formatted_datetime(self):
    date = '2020, 5, 17'
    self.assertRaises(TypeError, cast(date, 1).todatetime())