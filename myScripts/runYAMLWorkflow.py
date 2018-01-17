from heppy.framework.heppy_loop import * 
import yaml
from importlib import import_module

def runYAMLWorkflow(yamlConf)

  saveFolder = yamlConf["saveFolder"]

  os.system("mkdir -p " + saveFolder)

  steps = yamlConf["steps"]
  for step in steps:
    moduleName = step["module"]
    functionName = step["function"]
    print ">>>>> Executing", functionName, "..."
    try:
      function = getattr(import_module(moduleName), functionName)
    except AttributeError:
      print ">>>>> Error: can not find function", functionName, "in module", moduleName
      exit()
    function(yamlConf)


if __name__ == "__main__":
  parser = create_parser()

  options, other = parser.parse_args()

  # Getting the config file from the hreppy extra options
  for opt in options.extraOptions:
        if "=" in opt:
            (key, val) = opt.split("=", 1)
            if key == "ConfigFile":
              configFile = val

  yamlConf = yaml.load(file(configFile, 'r'))
  runYAMLWorkflow(yamlConf)
