#command to git repository:
#   import subprocess
#   subprocess.run["git", "clone", "http://github.com/Christian-K9/Bartleby"])

import socket

host_machine = "127.0.0.1"
port = input("What Is The NC Port Number?")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host_machine, port))
    data = s.recv(1024)

print("Received:", data.decode())
