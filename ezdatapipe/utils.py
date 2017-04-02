# get data from, and send data to, files (yaml, json, toml), processes
# create output string based on template file and dictionary object

import jinja2
import sys, stat, os
import subprocess
import getopt
import re
import utils

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

def merge(source, destination):
   for key, value in source.items():
      if isinstance(value, dict):
         # get node or create one
         node = destination.setdefault(key, {})
         merge(value, node)
      else:
         destination[key] = value
   return destination

