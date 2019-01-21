import socket, json


# HOST = 'localhost'
# PORT = 5000
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, PORT))
# s.listen(1)
# conn, addr = s.accept()
# while 1:
#     data = conn.recv(4096)
#     if not data: break
#     conn.send(data)
# conn.close()


class Server :

    def __init__(self, host='localhost', port=5000):
        self.__host = host
        self.__port = port

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((self.__host, self.__port))

        self.__conn = None
        self.__addr = None

    def establish_connection(self):
        self.__socket.listen(5)
        self.__conn, self.__addr = self.__socket.accept()

        self.__conn.send("OK")

    def send_data(self, world):
        json_data = json.dumps(world)

        self.__conn.send(json_data)

    def receive_data(self):
        return self.__conn.recv(4096)

    def close_connection(self):
        self.__socket.close()


Server().establish_connection()