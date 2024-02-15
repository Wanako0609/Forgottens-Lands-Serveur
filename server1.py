import pickle
import socket
import time
from _thread import *

import pygame.time
from src.entities.player import Player
from src.queuerecv import QueueRecv
import src.network.network as net

s = net.create_network()

players = []  # Listes des joueurs


def threaded_client(conn):
    player = net.connection(conn)

    print(player.get_stat())

    # ajout des joueurs dans la liste des joueurs connecté
    players.append(player)

    # Print debut queue
    # Queue
    queue = QueueRecv(conn)
    queue.start_thread()

    print("running")

    clock = pygame.time.Clock()
    while True:
        clock.tick(20)
        try:

            # Reponse a request
            if not queue.queue.empty():
                data = queue.queue.get()
                #print(data)

                if data["label"] == "update_request":
                    request = data["data"]

                    if request == "player_data":
                        # Envoie les players data du joueur courrant
                        player_data = player.get_stat()
                        net.send_data(conn, label="player_data", data=player_data)

                    elif request == "nb_players":
                        nb_players = str(len(players))
                        net.send_data(conn, label="nb_players", data=nb_players)

                    elif request == "other_players":
                        net.send_data(conn, label="other_players_start", data="start")
                        for other_player in players:
                            other_player_data = other_player.get_stat()
                            net.send_data(conn, label="other_players", data=other_player_data)
                        net.send_data(conn, label="other_players_end", data="ok")

                # GESTION METHODES (recv) #############################
                # Move
                elif data["label"] == "player_move":
                    player_move = data["data"]
                    #player.move(player_move)
                    print(player_move)

                # Action Color
                elif data["label"] == "action":
                    action = data["data"]
                    if action == "color":
                        print("color")
                        #player.change_color()

        except Exception as e:
            #print(e)
            queue.stop_thread()
            for player in players:
                if player.uuid == player.uuid:
                    players.remove(player)
                    break

            print("Player deconnecter")
            conn.close()
            break

    print("Connection Perdu")


while True:
    conn, addr = s.accept()  # accept incomming connection
    print("Conncted to:", addr)

    start_new_thread(threaded_client, (conn,))
