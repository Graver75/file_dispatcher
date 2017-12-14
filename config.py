import sys

PORT = int(sys.argv[1])
WANNA_CONTROL_SERVER = bool(int(sys.argv[2]))
BOOTSTRAP_LIST = sys.argv[3:]
FILE_DIRECTORY = './pub'

RECOVERY_DELAY = 120
PING_INTERVAL = min(RECOVERY_DELAY, 5)
GETADDR_INTERVAL = 10
GETFILENAMES_INTERVAL = 30