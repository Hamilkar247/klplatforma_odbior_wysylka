from shared_memory_dict import SharedMemoryDict
from time import sleep

smd_config = SharedMemoryDict(name='config', size=1024)

if __name__ == "__main__":
    while True:
        print(smd_config["status"])
        sleep(1)