from heppy.framework.heppy_loop import * 
import yaml
from importlib import import_module
from multiprocessing import Process, Queue

def functionWrapper(queue, function, yamlConf):
  function(yamlConf)
  queue.put(yamlConf)


def runYAMLWorkflow(yamlConf):

  saveFolder = yamlConf["saveFolder"]

  os.system("mkdir -p " + saveFolder)
  #os.system("cp " + yamlConf["ConfigFile"] + " " + saveFolder)
  saveTo = saveFolder + "/" + os.path.split(yamlConf["ConfigFile"])[1]
  with open(saveTo, 'w+') as dest_yaml_file:
    dump = yaml.dump(yamlConf, default_flow_style = False, allow_unicode = True, encoding = None)
    dest_yaml_file.write( dump )

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

    
    if ("__debugMode" in yamlConf) and (yamlConf["__debugMode"]):
      function(yamlConf)
    else:
      queue = Queue()
      functionProcess = Process(target=functionWrapper, args=(queue, function, yamlConf))
      functionProcess.start()
      functionProcess.join()
      yamlConf = queue.get()



if __name__ == "__main__":
  parser = create_parser()

  options, other = parser.parse_args()

  # Getting the config file from the heppy extra options
  for opt in options.extraOptions:
        if "=" in opt:
            (key, val) = opt.split("=", 1)
            if key == "ConfigFile":
              configFile = val

  yamlConf = yaml.load(file(configFile, 'r'))
  for opt in options.extraOptions:
        if "=" in opt:
            (key, val) = opt.split("=", 1)
            yamlConf[key] = val

  
  runYAMLWorkflow(yamlConf)
