import pickle
import socket
import threading
import time
from _thread import *
from player import Player
from queuerecv import QueueRecv

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # type connection

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen()
print("Serveur sur écoute")

players = []  # Listes des joueurs


def send_data(conn, label: str, data):
    labeled_data = {"label": label, "data": data}
    print("data send ", labeled_data)
    conn.send(pickle.dumps(labeled_data))


def connection(conn):
    # First message recoit l'uuid

    data = pickle.loads(conn.recv(2048))# Recv connection
    if data["label"] == "connection":
        uuid = data["data"]
    # uuid = conn.recv(2048).decode()
    # print("uuid " + uuid)

    # Crée le joueur coté serveur
    player = Player(uuid)
    # ajout des joueurs dans la liste des joueurs connecté
    players.append(player)
    # print(player.get_stat())

    # Envoie le ok
    send_data(conn, label="connection", data=player.get_stat())

    return player


def threaded_client(conn):
    player = connection(conn)

    # Queue
    queue = QueueRecv(conn)
    queue.start_thread()

    print("running")

    while True:
        try:
            # Actualisation du jeux
            time.sleep(0.005)
            # Player Data
            player_data = player.get_stat()
            send_data(conn, label="player_data", data=player_data)
            # Nb Player
            nb_players = str(len(players))
            send_data(conn, label="nb_players", data=nb_players)

            # Other Player Data
            send_data(conn, label="other_players_start", data="start")
            for other_player in players:
                other_player_data = other_player.get_stat()
                send_data(conn, label="other_players", data=other_player_data)
            send_data(conn, label="other_players_end", data="ok")


            # Reponse a request
            if not queue.queue.empty():
                data = queue.queue.get()
                print(data)

                if data["label"] == "update_request":
                    request = data["data"]

                    if request == "player_data":
                        # Envoie les players data du joueur courrant
                        player_data = player.get_stat()
                        send_data(conn, label="player_data", data=player_data)

                    elif request == "nb_players":
                        nb_players = str(len(players))
                        send_data(conn, label="nb_players", data=nb_players)

                    elif request == "other_players":
                        send_data(conn, label="other_players_start", data="start")
                        for other_player in players:
                            other_player_data = other_player.get_stat()
                            send_data(conn, label="other_players", data=other_player_data)
                        send_data(conn, label="other_players_end", data="ok")
        except Exception as e:
            print(e)
            for player in players:
                if player.uuid == player.uuid:
                    players.remove(player)
                    break

            print("Player deconnecter")
            conn.close()
            break

    assert False, "Connection Perdu"


while True:
    conn, addr = s.accept()  # accept incomming connection
    print("Conncted to:", addr)

    start_new_thread(threaded_client, (conn,))
