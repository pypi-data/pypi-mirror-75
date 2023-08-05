from datetime import datetime, date
from dateutil.parser import parse

class cast:
  """cast(datetime) -> returns str

     cast(datetime, format) -> returns str

     cast(str) -> returns str

     cast(List) -> finds datetime in List

     cast(Dict) -> finds datetime in Dict 

  """
  def __new__(cls, data, format = None):
    self = object.__new__(cls)
    self._data = data
    self._format = format
    return self

  def tostr(self):
    """ smart conversion of self._data"""
    if type(self._data) is str:
      return self._data

    elif type(self._data) is datetime or type(self._data) is date:
      return self.convert_to_str(data=self._data)

    elif type(self._data) is list:
      return self.convert_to_str_from_list(data=self._data, format=self._format)

    elif type(self._data) is dict:
      return self.convert_to_str_from_dict(data=self._data, format=self._format)

  def todatetime(self):
    """ smart conversion of self._data"""
    if type(self._data) is str:
      return self.convert_to_datetime()

    elif type(self._data) is datetime or type(self._data) is date:
      return self._data

    elif type(self._data) is list:
      return self.convert_to_datetime_from_list(data=self._data, format=self._format)

    elif type(self._data) is dict:
      return self.convert_to_datetime_from_dict(data=self._data, format=self._format)
      
      
  def replace_data(self, data = None):
    """ get convertable data """
    if data is None:
      return self._data
    return data

  def convert_to_formatted_str(self, data = None, format = None):
    """ convert a formatted str """
    data = self.replace_data(data=data)
      
    if format is not None:
      try:
        if type(data) is date:
          return date.strftime(data, format)
        return datetime.strftime(data, format)
      except TypeError as e:
        print("Datetime was not properly converted in date_reclass")
        print(e)
    return None

  def convert_to_str(self, data = None, format = None):
    """ convert datetime to str """
    data = self.replace_data(data)
    if format is not None:
      return self.convert_to_formatted_str(data=data, format=format)
      
    if self._format is not None:
      return self.convert_to_formatted_str(data=data, format=self._format)

    return str(data)

  def convert_to_formatted_datetime(self, data = None, format = None):
    """ convert a formatted datetime """
    data = self.replace_data(data=data)
    if format is not None:
      try:
        if type(data) is date:
          data = datetime.combine(date.today(), datetime.min.time())
        return datetime.strptime(data, format)
      except TypeError as e:
        print("Datetime was not properly converted in date_reclass")
        print(e)
    return self._data

  def convert_to_datetime(self, data = None, format = None):
    """ convert str to datetime """
    data = self.replace_data(data=data)

    if format is not None:
      return self.convert_to_formatted_datetime(data=data, format=format)
    
    if self._format is not None:
      return self.convert_to_formatted_datetime(data=data, format=self._format)

    return parse(data)

  def convert_to_datetime_from_list(self, data, format = None):
    """ convert str to datetime from values in list"""
    newly_formated_data = data

    for index in range(len(newly_formated_data)):
      if type(newly_formated_data[index]) is dict:
        newly_formated_data[index] = self.convert_to_datetime_from_dict(data=newly_formated_data[index], format=format)
      elif type(newly_formated_data[index]) is list:
        newly_formated_data[index] = self.convert_to_datetime_from_list(data=newly_formated_data[index], format=format)
      elif type(newly_formated_data[index]) is str:
        newly_formated_data[index] = self.convert_to_datetime(data=newly_formated_data[index], format=format)

    return newly_formated_data

  def convert_to_datetime_from_dict(self, data, format = None):
    """ convert str to datetime from values in dict """
    newly_formated_data = data

    for key, value in newly_formated_data.items():
      if type(value) is dict:
        newly_formated_data[key] = self.convert_to_datetime_from_dict(data=value, format=format)
      elif type(value) is list:
        newly_formated_data[key] = self.convert_to_datetime_from_list(data=value, format=format)
      elif type(value) is str:
        newly_formated_data[key] = self.convert_to_datetime(data=value, format=format)

    return newly_formated_data

  def convert_to_str_from_list(self, data, format = None):
    """ convert datetime to str from values in list"""
    newly_formated_data = data

    for index in range(len(newly_formated_data)):
      if type(newly_formated_data[index]) is dict:
        newly_formated_data[index] = self.convert_to_str_from_dict(data=newly_formated_data[index], format=format)
      elif type(newly_formated_data[index]) is list:
        newly_formated_data[index] = self.convert_to_str_from_list(data=newly_formated_data[index], format=format)
      elif type(newly_formated_data[index]) is datetime or type(newly_formated_data[index]) is date:
        newly_formated_data[index] = self.convert_to_str(data=newly_formated_data[index], format=format)

    return newly_formated_data

  def convert_to_str_from_dict(self, data, format = None):
    """ convert datetime to str from values in dict """
    newly_formated_data = data

    for key, value in newly_formated_data.items():
      if type(value) is dict:
        newly_formated_data[key] = self.convert_to_str_from_dict(data=value, format=format)
      elif type(value) is list:
        newly_formated_data[key] = self.convert_to_str_from_list(data=value, format=format)
      elif type(value) is datetime or type(value) is date:
        newly_formated_data[key] = self.convert_to_str(data=value, format=format)

    return newly_formated_data


