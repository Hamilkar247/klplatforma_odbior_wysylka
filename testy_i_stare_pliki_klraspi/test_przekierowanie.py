import sys

fh = open("wyniki_test.txt", "w")
print('przekierowanie stdin :', not sys.stdin.isatty(),  file=fh)
print('przekierowanie stdout:', not sys.stdout.isatty(), file=fh)
print('przekierowanie stderr:', not sys.stderr.isatty(), file=fh)
fh.close()
