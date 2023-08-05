import json

def is_json(json_object):
  """ Check if value is json"""
  try:
    json.loads(json_object)
  except:
    return False
  return True