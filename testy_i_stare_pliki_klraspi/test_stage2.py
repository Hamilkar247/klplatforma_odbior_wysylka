# stage2.py
import time
class Stage2:
  def stage2(self, queueS1, queueS2):
    print("def: stage2")
    while True:
        msg = queueS1.get()    # wait till there is a msg from s1
        print("- - - stage2 otrzymalem z s1:", msg)
        if msg == 's1 jest zakonczone ':
            break # ends loop
        time.sleep(1) # work
        queueS2.put("lista zaktualizowana")             
