import application
import importlib
import argparse
import os

#getting arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument("-cfg_file", help = "The Name of the config file")
args = parser.parse_args()

def start_with_std_cnfg():
    if os.listdir().__contains__("user_config.py"):
        import user_config
        application.main(user_config)
    else:
        print("No file named user_config.py exists, make sure, you haven't renamed the file, nor deleted it.")


if args.cfg_file != None: #a config file was parsed
    if os.listdir().__contains__(args.cfg_file.removesuffix(".py")+".py"):
        application.main(importlib.import_module(args.cfg_file.removesuffix(".py")))
    else:
        print("Wrong Module Name, starting with standard config file")
        start_with_std_cnfg()
else:
    start_with_std_cnfg()
