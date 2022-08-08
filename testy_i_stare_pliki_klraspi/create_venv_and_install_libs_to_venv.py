import os
import subprocess

def main():
    print("ahoj")

if __name__ == "__main__":
    bash_command="virtualenv venv".split()
    process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(f"stdout: {stdout}")
    print(f"stderr: {stderr}")
    ######
    bash_command="pip3 install --target="
