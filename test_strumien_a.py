import sys 
import os
import time
import signal
#SIGPIPE - obsługa przerwań
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

while True:
    #print("a\n")
    #time.sleep(0.1)
    line = sys.stdin.readline()
    if not line:
        break
#        line = input()
#    except EOFError:
#        break # lub exit(0)

#    print(line)
    line = "kurlaa:"+line
    sys.stdout.write(line)
    time.sleep(2)
