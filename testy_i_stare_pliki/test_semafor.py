import threading
import time
import logging
import pomiar_rtl_433

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class ThreadPool(object):
    def __init__(self):
        super(ThreadPool, self).__init__()
        self.active = []
        self.lock = threading.Lock()
    def makeActive(self, name):
        with self.lock:
            self.active.append(name)
            logging.debug('Running-Aktywacja: %s', self.active)
    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)
            logging.debug('Running-Deaktywacja: %s', self.active)

def f(s, pool, czas):
    logging.debug('Waiting to join the pool')
    with s:
        name = threading.current_thread().getName()
        pool.makeActive(name)
        time.sleep(czas)
        pool.makeInactive(name)

if __name__ == '__main__':
    pool = ThreadPool()
    s = threading.Semaphore(19)
    czas=5
    for i in range(9):
        czas=czas+5
        t = threading.Thread(target=f, name='thread_'+str(i), args=(s, pool, czas))
        t.start()
