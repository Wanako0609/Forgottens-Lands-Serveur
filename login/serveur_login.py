import socket
from _thread import *
import os
import json
import uuid
import bcrypt

# Gestion Serveur
server = "127.0.0.1"
port = 5566

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")


def str_list(string):
    liste_data = string.split(",")
    return [liste_data[0], liste_data[1], liste_data[2]]


def list_str(liste):
    return str(liste[0]) + "," + str(liste[1]) + "," + str(liste[2])


def hash_mot_de_passe(mot_de_passe):
    # Générer un hachage de mot de passe avec bcrypt
    return bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())


def enregistrer_utilisateur(login, mot_de_passe):
    fichier_json_login = f"../data/login/{login}.json"

    if os.path.exists(fichier_json_login):
        print(f"Le compte avec le login '{login}' existe déjà.")
        return
        # Pas oublié ici

    # Générer un UUID unique pour l'utilisateur
    utilisateur_uuid = str(uuid.uuid4())

    # Hacher le mot de passe
    mot_de_passe_hache = hash_mot_de_passe(mot_de_passe)

    # Créer un dictionnaire avec les données de l'utilisateur
    utilisateur = {
        "login": login,
        "uuid": utilisateur_uuid,
        "mot_de_passe": mot_de_passe_hache.decode('utf-8'),  # Ne pas décodez le hachage
    }

    # Créer un fichier JSON avec le nom du login de l'utilisateur
    with open(fichier_json_login, 'w') as fichier:
        json.dump(utilisateur, fichier)

    print(f"Utilisateur enregistré avec succès. Fichier JSON (login) : {fichier_json_login}")

    # Créer un fichier JSON avec le nom de l'UUID de l'utilisateur pour les statistiques
    fichier_json_stats = f"../data/playerdata/{utilisateur_uuid}.json"
    stats_joueur = {
        "x": 100,
        "y": 50,
        "color": (0,255,0),
        # Ajoutez d'autres statistiques selon vos besoins
    }

    with open(fichier_json_stats, 'w') as fichier_stats:
        json.dump(stats_joueur, fichier_stats)

    print(f"Fichier JSON (stats) créé avec succès. UUID : {utilisateur_uuid}")


def verifier_mot_de_passe(login, mot_de_passe):
    # Charger les données de l'utilisateur depuis le fichier JSON
    fichier_json_login = f"../data/login/{login}.json"
    try:
        with open(fichier_json_login, 'r') as fichier:
            utilisateur = json.load(fichier)

            # Vérifier le mot de passe
            if bcrypt.checkpw(mot_de_passe.encode('utf-8'), utilisateur["mot_de_passe"].encode('utf-8')):
                print("Connexion réussie.")
                #print("Données de l'utilisateur :", utilisateur)

                # Charger les statistiques depuis le fichier JSON
                #fichier_json_stats = f"../data/playerdata/{utilisateur['uuid']}.json"
                #with open(fichier_json_stats, 'r') as fichier_stats:
                #    stats_joueur = json.load(fichier_stats)

                #print("Statistiques du joueur :", stats_joueur)

                return utilisateur['uuid']
            else:
                print("Mot de passe incorrect.")
                return "Mot de passe incorrect."

    except FileNotFoundError:
        print("Utilisateur non trouvé.")
        return "Utilisateur non trouvé."


def login_existe(login):
    return os.path.exists(f'../data/login/{login}.json')


def threaded_client(conn):

    reply = ""
    data = str_list(conn.recv(2048).decode())

    if not data:
        print("Disconnected")
    else:
        data_get = data
        if int(data_get[0]) == 0:
            if login_existe(data[1]):
                reply = verifier_mot_de_passe(data[1], data[2])
                #reply = "Connection tester"
            else:
                reply = "Pas d'utilisateur."

        elif int(data_get[0]) == 1:
            enregistrer_utilisateur(data[1], data[2])
            reply = verifier_mot_de_passe(data[1], data[2])

        print("Received: ", data)
        print("Sending : ", reply)

    conn.send(str.encode(reply))
    print("End connection")
    conn.close()


# Boucle d'action
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))
