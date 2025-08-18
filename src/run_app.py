import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-cfg_file", help = "The Name of the config file")
args = parser.parse_args()

subprocess.Popen(["pythonw.exe", "main.py", args])