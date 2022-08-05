from subprocess import Popen, PIPE, CalledProcessError

#inspiracja https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running

def main():
    cmd="rtl_433 -s 2.5e6 -f 868.5e6 -H 30 -R 75 -R 150 -F json".split(" ")
    
    with Popen(cmd, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='') # process line here
    
    if p.returncode != 0:
        raise CalledProcessError(p.returncode, p.args)

if __name__ == "__main__":
    main()
