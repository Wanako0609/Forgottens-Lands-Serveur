import socket
import pickle


class Network:

    def __init__(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.addr = (self.server, self.port)

        self.connection()

    def connection(self):
        try:
            self.server.bind((self.ip, self.port))
        except socket.error as e:
            print(str(e))

        self.server.listen()  # Arg how many person connected
        print("Waiting for a connection, Serveur Started")

    def rcv_obj(self, conn):
        nb_players = pickle.loads(self.server.recv(2048))  # pickle.loads() recompose l'object
        print(nb_players)
        self.server.send(str.encode("ok"))
        return nb_players

    def rcv_str(self, conn):
        received_str = self.server.recv(2048).decode("utf-8")
        print(received_str)
        self.server.send(str.encode("ok"))
        return received_str

    # Send information and receve respond
    def send_obj(self, data, conn):
        try:
            self.server.send(pickle.dumps(data))   # pickle.dump decompose l'object en binaire
            self.server.recv(2048).decode()  # Wait
        except socket.error as e:
            print(e)

    def send_str(self, data, conn):
        try:
            self.server.send(str.encode(data))
            self.server.recv(2048).decode()
        except socket.error as e:
            print(e)

    def close(self, conn): self.server.close()
