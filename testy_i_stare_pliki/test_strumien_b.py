import os
import sys
import time
import signal
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

for line in sys.stdin:
    sys.stdout.write(line)
#while True:
#    text = input()
#    text=text+"b"
#    print(text)
#print(f"Sen na {sec}")
#time.sleep(int(sec))
#print("Koniec")
