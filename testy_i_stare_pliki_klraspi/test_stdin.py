import signal
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

import sys

number = 0

for line in sys.stdin:
    number += 1

    #sys.stdout.write(f"{number} ")
    #sys.stdout.write(line)
    print(line)
    if number==111:
        break

