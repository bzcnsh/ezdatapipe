import utils as ezdputils
import tempfile
import os, stat, sys
import jinja2
import subprocess


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
   rtn = ezdputils.processTemplate(templateFile, templateVars)
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