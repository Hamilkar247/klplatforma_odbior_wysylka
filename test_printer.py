import sys
import os
import time
import signal
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

number = 1

while True:
    line = input()
    if not line:
        break

    number += 1

    sys.stdout.write(f"{number} ")
    sys.stdout.write(line)
    sys.stdout.write("\n")
