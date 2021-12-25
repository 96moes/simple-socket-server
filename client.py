import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.1.1', 12345))
data = input("please enter your string \n")
client.send(data.encode())
from_server = client.recv(4096)
client.close()
print(from_server.decode())

