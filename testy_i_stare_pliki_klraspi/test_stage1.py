# stage1.py
import time
import random
import subprocess
class Stage1:
  def stage1(self, queueS1, queueS2):
    print("def: stage1")
    lala = []
    #lis = [1, 2, 3, 4, 5]
    for i in range(10):
      lis = [i]
      # to avoid unnecessary waiting
      if not queueS2.empty():
        msg = queueS2.get()    # get msg from s2
        print("! ! ! stage1 otrzymal z s2:", msg)
        #lala = [6, 7, 8] # now that a msg was received, further msgs will be different
      time.sleep(2) # work
      #random.shuffle(lis)
      command=f"timeout 10 rtl_433 -s 2.5e6 -f 868.5e6 -H 30 -R 75 -R 150 -F json".split(" ")
      process = subprocess.Popen(command,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          #shell=True,
                          #preexec_fn=os.setsid
                          )
      stdout, stderr = process.communicate()
      print(stderr)
      queueS1.put(stdout)             
    queueS1.put('s1 jest zakonczonee')