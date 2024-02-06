import os
import json
import player


def create_stats():
    information = {
        "uuid": "",
    }
    stat = {
        "max_health": 100,
        "health": 50,
        "Strenght": 10,
        "Crit_Value": 0,
        "Armor": 10,
        "Speed": 3
    }
    pos = {
        "x": 0,
        "y": 0,
        "map": None
    }

    stats = {
        "stats": stat,
        "pos": pos
    }
    return stats


class Playerdata:

    def __init__(self, uuid):
        self.uuid = uuid
        self.x = 0
        self.y = 0
        self.width = 100
        self.height = 100
        self.speed = 3

        # Init
        self.color = self.get_color()
        self.get_pos()

    # A utilisé avec les vrai joueurs
    def get_stat(self):
        # Charger les statistiques depuis le fichier JSON
        fichier_json_stats = f"../data/playerdata/{self.uuid}.json"
        #print("file " + fichier_json_stats)
        with open(fichier_json_stats, 'r') as fichier_stats:
            stats_joueur = json.load(fichier_stats)
        return stats_joueur

    def get_pos(self):
        stats = self.get_stat()
        self.x = stats['x']
        self.y = stats['y']
        return self.x, self.y

    def set_pos(self):
        modifier_valeurs_json(f"../data/playerdata/{self.uuid}.json", {"x": self.x, "y": self.y})

    # Temporaire
    def get_color(self):
        stats = self.get_stat()
        self.color = stats['color']
        return stats['color']

    # Temporaire
    def set_color(self, color):
        self.color = color
        modifier_valeurs_json(f"../data/playerdata/{self.uuid}.json", {"color": color})



def modifier_valeurs_json(fichier_json, modification):
    # Charger le fichier JSON existant
    with open(fichier_json, 'r') as fichier:
        donnees = json.load(fichier)

    # Appliquer les modifications nécessaires dans la structure de données Python
    for cle, valeur in modification.items():
        donnees[cle] = valeur

    # Écrire les données mises à jour dans le fichier JSON
    with open(fichier_json, 'w') as fichier:
        json.dump(donnees, fichier, indent=2)

