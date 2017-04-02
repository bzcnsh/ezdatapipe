import yaml, toml, json
import os

def saveToFile(text, filename):
   of = open(filename, 'w')
   of.write(text)
   of.close()

def accessDataFile(filename, action, format=None):
   knownExtensionFormats = {'.yml': 'yaml', '.yaml': 'yam', '.jsn': 'json', '.json': 'json', '.toml': 'toml'}
   accessFormattedFile={
     'yaml': {'read': readYamlFile, 'write': writeYamlFile},
     'json': {'read': readJsonFile, 'write': writeJsonFile},
     'toml': {'read': readTomlFile, 'write': writeTomlFile}
   }
   try:
      if not format:
         extension = os.path.splitext(filename)[1].lower()
         format = knownExtensionFormats[extension]
      return accessFormattedFile[format][action]
   except:
      print "missing or unsupported format or action"
      raise

def readDataFile(filename, format=None):
   return accessDataFile(filename, 'read', format)(filename)

def writeDataFile(filename, data, format=None):
   accessDataFile(filename, 'write', format)(filename, data)

def readYamlFile(filename):
   with open(filename, 'r') as stream:
      return yaml.load(stream)

def writeYamlFile(filename, data):
   with open(filename, 'w') as outfile:
      yaml.dump(data, outfile, default_flow_style=False)

def readYamlText(text):
   return yaml.load(text)

def readJsonFile(filename):
   with open(filename, 'r') as stream:
      return json.load(stream)
      #return json_load_byteified(stream)

def writeJsonFile(filename, data):
   with open(filename, 'w') as outfile:
      json.dump(data, outfile)

def readJsonText(text):
   return json.load(text)

def readTomlFile(filename):
   with open(filename, 'r') as stream:
      return toml.loads(stream.read())

def writeTomlFile(filename, data):
   with open(filename, 'w') as outfile:
      outfile.write(toml.dumps(data))

def readTomlText(text):
   return toml.loads(text)

# --- http://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-ones-from-json-in-python
def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data

# ----------
