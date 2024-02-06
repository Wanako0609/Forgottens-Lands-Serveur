import pickle
import socket
from _thread import *

import pygame

from player import Player

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # type connection

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen()  # Arg how many person connected
print("Waiting for a connection, Serveur Started")

# Gestion sauvegarde
# Automatiquement en les recuperant du player data
players = []  # Les positions par defaut des joueurs dans des tupples


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
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        try:
            # GESTION ACTUALISATION JOUEUR #############################

            # Envoie les players data du joueur courrant
            conn.send(pickle.dumps(player.get_stat()))
            conn.recv(2048).decode()  # Wait

            # Envoie des players actuellement connecté
            # print(f"Il y a {nb_players} joueurs co et type {type(nb_players)}")
            nb_players = str.encode(str(len(players)))
            conn.send(nb_players)
            conn.recv(2048).decode()  # Wait

            # Envoie la liste des joueurs connecté avec leurs informations imperative pour le jeux et pas le reste
            for other_player in players:
                conn.send(pickle.dumps(other_player.get_stat()))
                conn.recv(2048)  # Wait

            # GESTION METHODES #############################

            # Gestion des methodes coté client

            # Move
            keys_move = pickle.loads(conn.recv(2048))
            conn.send(str.encode("ok"))  # Wait
            player.move(keys_move)

            # Action Color
            # Seule action est la couleur
            data = pickle.loads(conn.recv(2048))
            conn.send(str.encode("ok"))  # Wait
            if data[0] == 1:
                player.change_color()

            """
            if not data:
                print("Disconnected")
                break
            else:
                if currentplayer == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                # data est ce que on a recu
                # reply est le tuple du joueur modifier
                print("Recieved ", data)
                print("Sending : ", reply)
    
            # Convertir reply en str
            conn.sendall(pickle.dumps(reply))  # encode in to au bit object
            
            """
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
