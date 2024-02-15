import socket
import pickle
import threading
from ..entities.player import Player


def create_network():
    server = "127.0.0.1"
    port = 5555

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # type connection

    try:
        s.bind((server, port))
    except socket.error as e:
        print(str(e))

    s.listen()
    print("Serveur sur écoute")
    return s


def send_data(conn, label: str, data):
    # Lancer le thread de send data
    threading.Thread(target=send_data_2, args=(conn, label, data)).start()


def send_data_2(conn, label: str, data):
    labeled_data = {"label": label, "data": data}
    print("data send ", labeled_data)
    try:
        conn.send(pickle.dumps(labeled_data))
    except BrokenPipeError:
        print("Erreur : Connexion interrompue.")
    except ConnectionResetError:
        print("Erreur : Connexion réinitialisée par le pair.")
    except socket.error as e:
        print(f"Erreur de socket : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")



def connection(conn):
    # First message recoit l'uuid

    data = pickle.loads(conn.recv(2048))  # Recv connection
    if data["label"] == "connection":
        uuid = data["data"]
    # uuid = conn.recv(2048).decode()
    # print("uuid " + uuid)

    # Crée le joueur coté serveur
    player = Player(uuid)

    # Envoie le ok
    send_data(conn, label="connection", data=player.get_stat())

    return player
