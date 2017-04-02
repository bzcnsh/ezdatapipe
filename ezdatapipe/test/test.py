import sys
import os

import unittest
import ezdatapipe.utils
import ezdatapipe.cmd
import ezdatapipe.io
import ezdatapipe.filter

test_dir = os.path.dirname(os.path.realpath(__file__))

class UtilitiesTestCase(unittest.TestCase):
   def setUp(self):
      print("setup")
      self.testdict = {'key1': 'val1', 'key2': 'val2', 'key3': ['text', 'text2'] }

   def tearDown(self):
      print("tear down")

   def test_runProcess(self):
      cmd = ["echo", "test"]
      rtn = ezdatapipe.cmd.runProcess(cmd)
      expected = {'returncode': 0, 'stdout': "test\n", 'stderr': "", 'cmd': cmd}
      self.assertEqual(rtn, expected)

   def test_runProcessFromTemplate(self):
      rtn = ezdatapipe.cmd.runProcessFromTemplate(test_dir + '/runProcessFromTemplateTest', {'instring': 'test'})
      del rtn['cmd']
      expected = {'returncode': 0, 'stdout': "test\n", 'stderr': "", 'command_text': "#!/bin/bash\necho test"}
      self.assertEqual(rtn, expected)

   def test_runProcessFromTemplate_not_exist(self):
      rtn = ezdatapipe.cmd.runProcessFromTemplate(test_dir + '/runProcessFromTemplateTest_not_here', {'instring': 'test'})
      del rtn['cmd']
      expected = {'returncode': 1, 'stdout': "", 'stderr': "An exception of type TemplateNotFound occurred. Arguments:\n()"}
      self.assertEqual(rtn, expected)

   def test_runProcessFromTemplateString(self):
      rtn = ezdatapipe.cmd.runProcessFromTemplateString("#!/bin/bash\necho {{instring}}", {'instring': 'test'})
      del rtn['cmd']
      expected = {'returncode': 0, 'stdout': "test\n", 'stderr': "", 'command_text': "#!/bin/bash\necho test"}
      self.assertEqual(rtn, expected)

   def test_runProcessFromTemplateString_badtemplate(self):
      rtn = ezdatapipe.cmd.runProcessFromTemplateString("", {'instringaaa': 'test'})
      self.assertNotEqual(rtn['returncode'], 0)
      self.assertTrue('exception' in rtn['stderr'])
   #write python dict to file
   #read data back
   def test_read_write_DataFile(self):
      self.assertEqual(self.write_read('/tmp/test.yml'), self.testdict)
      self.assertEqual(self.write_read('/tmp/test.json'), self.testdict)
      self.assertEqual(self.write_read('/tmp/test.toml'), self.testdict)

   def write_read(self, filename):
      ezdatapipe.io.writeDataFile(filename, self.testdict)
      return ezdatapipe.io.readDataFile(filename)

   def test_filter_data_by_path(self):
      testdict = {'key1': 'val1', 'key2': 'val2', 'key3': ['text', {'key4': 'val4'}, 'text2'] }
      nodes = []
      ezdatapipe.filter.filter_data_by_path(testdict, [], ["\\.key4$"], nodes)
      self.assertEqual(nodes, ['val4'])


# def runProcess(cmd):
# def runProcessFromTemplate(templateFile, templateVars):
# def runProcessFromTemplateString(template_string, templateVars):
# def runProcessFromString(cmd_string):
# def filter_data_by_path(source, path, path_pattern, nodes):
# def readCLI(cli_opts):
# def processTemplate(templateFile, templateVars):
# def json_load_byteified(file_handle):
# def json_loads_byteified(json_text):
# def _byteify(data, ignore_dicts = False):
# def saveToFile(text, filename):
# def merge(source, destination):
# def accessDataFile(filename, action, format=None):
# def readDataFile(filename, format=None):
# def writeDataFile(filename, data, format=None):
# def readYamlFile(filename):
# def writeYamlFile(filename, data):
# def readYamlText(text):
# def readJsonFile(filename):
# def writeJsonFile(filename, data):
# def readJsonText(text):
# def readTomlFile(filename):
# def writeTomlFile(filename, data):
# def readTomlText(text):

if __name__ == '__main__':
   unittest.main()

