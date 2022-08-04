import sys
import os
import time
import signal
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

number=0
while True:
    print("A\n")
    time.sleep(0.1)
    number=number+1
    if number==6:
        break
