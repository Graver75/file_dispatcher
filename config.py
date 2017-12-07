import sys

PORT = int(sys.argv[1])
WANNA_CONTROL_SERVER = bool(int(sys.argv[2]))
BOOTSTRAP_LIST = sys.argv[3:]
FILE_DIRECTORY = './pub'