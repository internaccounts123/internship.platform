import socket, pickle

HOST = 'localhost'
PORT = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


data = s.recv(4096)
data = data.decode()
s.close()
print ('Received', repr(data))
