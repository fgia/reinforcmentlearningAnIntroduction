#################################################################
# Mise en oeuvre de la méthode monte carlo 
# TODO : 
#       - calcul de Q(S,A)
#       - recherche de la politique optimale
#################################################################

import numpy as np
from episode import Episode
from episode import Game
from etat import Etat
#Valeur de epsilon
epsilon = 0.001

# Etat final
PLAYER_WIN = 1
PLAYER_LOST = -1
PLAYER_DRAW = 0

#Nombre d'états 
STATE_NUMBER = 200
ACTION_NUMBER = 2

#Actions
#demande une carte
ACTION_HIT = 0
#Ne fait rien
ACTION_STICK = 1

#Politique
# policy for player
POLICY_PLAYER = np.zeros(200, dtype=np.int)
# policy for dealer
POLICY_DEALER = np.zeros(22)

# State action - valeur (200 états, 2 actions)
Q =  np.zeros((200, 2))

################################################# 
#
# Initialisation de la politique
#
#################################################
def init_politiques():
    # Définition de la politique du joueur (peut importe la carte du dealer et de usable_as)
    
    
    for i in range(12, 20):
        for j in range(12,20):
            POLICY_PLAYER[Etat.calcul_index(i,j,0)] = ACTION_HIT
            POLICY_PLAYER[Etat.calcul_index(i,j,1)] = ACTION_HIT
    for j in range(12,20):
        POLICY_PLAYER[Etat.calcul_index(20,j,0)] = ACTION_STICK
        POLICY_PLAYER[Etat.calcul_index(20,j,1)] = ACTION_STICK
        POLICY_PLAYER[Etat.calcul_index(21,j,0)] = ACTION_STICK
        POLICY_PLAYER[Etat.calcul_index(21,j,1)] = ACTION_STICK
    
    # Définition de la politique du joueur
    for i in range(0, 17):
        POLICY_DEALER[i] = ACTION_HIT
    for i in range(17, 22):
        POLICY_DEALER[i] = ACTION_STICK

################################################# 
#
# Renvoie une nouvelle carte
#
#################################################
def get_carte():
    card = np.random.randint(1, 14)
    card = min(card, 10)
    return card




################################################# 
#
# calcul du gagnant ou perdant
#
#################################################
def final_etat(valeurPlayer: int,valeurDealer: int):
    # en premier car 
    if (valeurPlayer>21):
        return PLAYER_LOST

    if (valeurDealer>21):
        return PLAYER_WIN

    if (valeurPlayer == valeurDealer):
        return PLAYER_DRAW    

    if (valeurPlayer > valeurDealer):
        return PLAYER_WIN
    
    return PLAYER_LOST


################################################# 
#
# Renvoie l'action suivante à partir de la politique
#   sum : somme des cartes du joueur
#   dealer_card: carte visible du dealer
#   usable_as : le joueur a t-il un usable _as?
#################################################
def politique_player(etat: Etat):
    index = etat.state_index()
    return POLICY_PLAYER[index]

################################################# 
#
# Next Episode
#
#################################################
def next_episode(episode: Episode):
    # execution de l'action
    action = episode.action
    if (action==ACTION_HIT):
            # nouvelle carte
            newcard = get_carte()
            gamePlayer = Game.calcul_value_player(episode.etat.player_value,newcard, episode.etat.as_usable)
            etat = Etat(gamePlayer.sum,episode.etat.dealer_card,gamePlayer.usable_as)
            episode = Episode(etat,-1,-1)
    return episode
################################################# 
#
# construit un épisode
#
#################################################
def play_episodes():
    episodes = []
    # Choisi un etat et une action de départ
    ######################################################################
    # Un état = 2 cartes pour le joueur , carte visible du dealer
    card_player_1 = get_carte()
    card_player_2 = get_carte()
    # on détermine si initialement il y a un as initialement
    usable_as_init = 0
    if card_player_1==1:
        usable_as_init =1
    # calcul de l'état initial
    gamePlayer = Game.calcul_value_player(card_player_1,card_player_2,usable_as_init);
    # on doit commencer à 12
    while(gamePlayer.sum<12):
        gamePlayer = Game.calcul_value_player(gamePlayer.sum,get_carte(),gamePlayer.usable_as)
    
    #####################################################################
    # détermination des cartes pour le dealer
    card_dealer_visible_1 = get_carte()
    card_dealer_2 = get_carte()
    usable_as_init = 0
    if card_player_1==1:
        usable_as_init =1
    
    gameDealer = Game.calcul_value_player(card_dealer_visible_1,card_dealer_2,usable_as_init);
    while(gameDealer.sum<12):
        gameDealer = Game.calcul_value_player(gameDealer.sum,get_carte(),gameDealer.usable_as)
    
    #######################################################################
    # Episodes du joueur
    etatPlayer = Etat(gamePlayer.sum,gameDealer.sum,gamePlayer.usable_as)
    episode = Episode(etatPlayer, -1, 0)
    episodes.append(episode)
    while True:
        # Action suivante
        actionPlayer = politique_player(etatPlayer)
        # Sauvegarde l'action
        episode.action = actionPlayer
        # stick = arrête
        if actionPlayer == ACTION_STICK:
            break
        # Execute l'action
        episode = next_episode(episode)
        episodes.append(episode)
        # player recompense
        if (episode.etat.player_value > 21):
            break
        if (episode.etat.player_value == 21):
            #pas de récompense car dépend du résultat du dealer
            break
    
    #######################################################################
    # Episodes du joueur
    etatDealer = Etat(gameDealer.sum,0,gameDealer.usable_as)
    episodeDealer = Episode(etatDealer, -1, 0)
    while True:
        # Action suivante
        actionDealer = POLICY_DEALER[gameDealer.sum]
        # on s'arrête
        if actionDealer == ACTION_STICK:
            break
        # Execute l'action   
        episodeDealer =   next_episode(episodeDealer)
        # player recompense
        if (episodeDealer.etat.player_value > 21):
            episodeDealer.recompense = -1;
            break
        if (episodeDealer.etat.player_value == 21):
            #pas de récompense car dépend du résultat du joueur
            break
    print("Episode Player", episode.etat.player_value)
    print("Episode Dealer", episodeDealer.etat.player_value)

    #Détermination de la récompense du joueur
    recompense = final_etat(episode.etat.player_value,episodeDealer.etat.player_value)
    episode.recompense = recompense


if __name__ == '__main__':
    print('Démarrage')
    print("Initialisation des données")
    init_politiques()
    play_episodes()