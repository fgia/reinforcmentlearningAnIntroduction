from etat import Etat
class Episode:
    etat: Etat
    action:int
    recompense: int
    def __init__(self,etat: Etat,action: int, recompense: int=0):
        self.etat = etat
        self.action = action
        self.recompense = recompense

class Game:
    sum: int
    usable_as: int
    def __init__(self,sum: int, usable_as:int):
        self.sum = sum
        self.usable_as = usable_as
################################################# 
#
# indique si l'as est usable
#
#################################################
    def is_usable_as(initvalue: int,newcard: int):
        if (newcard ==1):
            if (initvalue + 11) <22:
                return 1
        return 0

################################################# 
#
# calcul la valeur du joueur
#
#################################################
    def calcul_value_player(initvalue: int, newcard: int, usable: int):
        valeur = initvalue + newcard
        usable_as = 0
        # Cas de l'as "11 ou 1"
        if (Game.is_usable_as(initvalue,newcard )):
            valeur =  initvalue + 11
            # l'as peu repasser à 1
            usable_as = 1 
        #As-ton un As usable
        if (valeur>21):
            if (usable>0):
                valeur =  valeur - 10
                # plus d'as usable
                usable = 0
    
        game = Game(valeur,usable + usable_as)

        return game   