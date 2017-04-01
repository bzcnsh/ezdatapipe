# get data from, and send data to, files (yaml, json, toml), processes
# create output string based on template file and dictionary object

import jinja2
import yaml, toml, json
import sys, stat, os
import subprocess
import getopt
import tempfile
import re

# runProcess(cmd)
# runProcessFromTemplate(templateFile, templateVars)
# runProcessFromTemplateString(template_string, templateVars)
# runProcessFromString(cmd_string)
# filter_data_by_path(source, path, path_pattern, nodes)
# readCLI(cli_opts)
# processTemplate(templateFile, templateVars)
# json_load_byteified(file_handle)
# json_loads_byteified(json_text)
# _byteify(data, ignore_dicts = False)
# saveToFile(text, filename)
# merge(source, destination)
# accessDataFile(filename, action, format=None)
# readDataFile(filename, format=None)
# writeDataFile(filename, data, format=None)
# readYamlFile(filename)
# writeYamlFile(filename, data)
# readYamlText(text)
# readJsonFile(filename)
# writeJsonFile(filename, data)
# readJsonText(text)
# readTomlFile(filename)
# writeTomlFile(filename, data)
# readTomlText(text)


# description: runs a process and capture all its output, stdin is implicitly passed to
# the new process
#
# parameters:
#    cmd: a list of tokens
#
# output:
#    a dictionary with these keys:
#      returncode
#      stdout
#      stderr
#      cmd
def runProcess(cmd):
   rtn = {'returncode': 0, 'stdout': "", 'stderr': "", 'cmd': cmd}
   try:
      popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      p_rtn = popen.communicate(input=sys.stdin)
      rtn['returncode']=popen.returncode
      rtn['stdout']=p_rtn[0]
      rtn['stderr']=p_rtn[1]
   except Exception as ex:
      rtn['returncode']=1
      rtn['stderr'] = "An exception of type {0} occurred. Arguments:\n{1!r}".format(type(ex).__name__, ex.args)
      pass
   return rtn

# description: create a shell script based on a template, then run it
#
# parameters:
#    templateFile: path to template
#    templateVars: variable to update placeholders in template
# output:
#    a dictionary with these keys:
#      all keys from runProcess
#      command_text: generate command from template

def runProcessFromTemplate(templateFile, templateVars):
   rtn = processTemplate(templateFile, templateVars)
   if rtn['returncode']==0:
      return runProcessFromString(rtn['stdout'], 'keepTempFile' in templateVars)
   else:
      rtn['cmd']="processTemplate({}, {})".format(templateFile, templateVars)
      return rtn

def runProcessFromTemplateString(template_string, templateVars):
   template = jinja2.Template(template_string)
   cmd_text = template.render(templateVars)
   return runProcessFromString(cmd_text, 'keepTempFile' in templateVars)

def runProcessFromString(cmd_text, keepTempFile):
   temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
   temp_file_name = temp_file.name
   temp_file.write(cmd_text)
   temp_file.close()
   os.chmod(temp_file_name, stat.S_IXUSR|stat.S_IRUSR)
   rtn = runProcess([temp_file_name])
   rtn['command_text'] = cmd_text
   if not keepTempFile:
      os.remove(temp_file_name)
   return rtn
    
# description: traverse a data structure and capture nodes whose path matches patterns
#
# parameters:
#    source: data to be traversed
#    path: bi-directional parameter, to keep track of current location
#    path_pattern: a list of patterns to be found in path
#    nodes: bi-directional parameter, to keep track of matched nodes
# output:
#    nodes: bi-directional parameter, to keep track of matched nodes

def filter_data_by_path(source, path, path_pattern, nodes):
    string_path = ".".join(path)
    for p in path_pattern:
        if re.search(p, string_path):
            nodes.append(source)
    if isinstance(source, dict):
        for k in source:
            path.append(k)
            traverse_data(source[k], path, path_pattern, nodes)
            path.pop()
    if isinstance(source, list):
        for i, v in enumerate(source):
            path.append("["+str(i)+"]")
            traverse_data(v, path, path_pattern, nodes)
            path.pop()

def readCLI(cli_opts):
   cli_opts_shorts = map(lambda x:(x['short'] if not x['has_value'] else x['short']+':'), cli_opts)
   cli_opts_longs = map(lambda x:(x['long'] if not x['has_value'] else x['long']+'='), cli_opts)
   cli_opts_all = map(lambda x:['-'+x['short'], '--'+x['long']], cli_opts)

   opts, remainder = getopt.getopt(sys.argv[1:], ''.join(cli_opts_shorts), cli_opts_longs)
   options = {}
   for opt, arg in opts:
      for index, value in enumerate(cli_opts_all):
         if opt in value:
            opt_name = cli_opts[index]['long']
            if opt_name in options:
               options[opt_name].append(arg)
            else:
               options[opt_name] = [arg]
            break
   return options

def processTemplate(templateFile, templateVars):
   rtn = {'returncode': 0, 'stdout': "", 'stderr': ""}
   try:
       templateLoader = jinja2.FileSystemLoader( searchpath=os.path.dirname(templateFile) )
       templateEnv = jinja2.Environment( loader=templateLoader )
       template = templateEnv.get_template( os.path.basename(templateFile) )
       outputText = template.render( templateVars )
       rtn['stdout'] = outputText
   except Exception as ex:
       rtn['returncode'] = 1
       rtn['stderr'] = "An exception of type {0} occurred. Arguments:\n{1!r}".format(type(ex).__name__, ex.args)
       pass
   return rtn

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

def saveToFile(text, filename):
   of = open(filename, 'w')
   of.write(text)
   of.close()

def merge(source, destination):
   for key, value in source.items():
      if isinstance(value, dict):
         # get node or create one
         node = destination.setdefault(key, {})
         merge(value, node)
      else:
         destination[key] = value
   return destination

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

