import pickle
import socket
import threading
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


def threaded_client(conn):
    # First message recoit l'uuid
    uuid = conn.recv(2048).decode()
    # print("uuid " + uuid)

    # Crée le joueur coté serveur
    player = Player(uuid)
    # ajout des joueurs dans la liste des joueurs connecté
    players.append(player)
    print(player.get_stat())

    # Envoie les players data du joueur courrant
    conn.send(pickle.dumps(player.get_stat()))

    # Queue
    queue = QueueRecv(conn)

    while True:
        try:

            # Envoie des players actuellement connecté
            # print(f"Il y a {nb_players} joueurs co et type {type(nb_players)}")

            # Envoie la liste des joueurs connecté avec leurs informations imperative pour le jeux et pas le reste


            # Gestion des méthodes côté client
            data = queue.get_queue().get(block=False)

            # GESTION ACTUALISATION JOUEUR (Send ) #############################
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
                    for other_player in players:
                        other_player_data = other_player.get_stat()
                        send_data(conn, label="other_players", data=other_player_data)
                else:
                    print("Mauvais format request")
                    print(request)

            # GESTION METHODES (recv) #############################
            # Move
            elif data["label"] == "player_move":
                player_move = data["data"]
                player.move(player_move)

            # Action Color
            elif data["label"] == "action":
                action = data["data"]
                if action == "color":
                    player.change_color()

        except Exception as e:
            print(e)
            for player in players:
                if player.uuid == uuid:
                    players.remove(player)
                    break

            print("Player deconnecter")
            conn.close()
            break


while True:
    conn, addr = s.accept()  # accept incomming connection
    print("Conncted to:", addr)

    start_new_thread(threaded_client, (conn,))
