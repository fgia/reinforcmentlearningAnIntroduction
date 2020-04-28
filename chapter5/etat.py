class Etat:
    player_value: int
    dealer_card: int
    as_usable: int

    def __init__(self,player_value: int, dealer_card: int, as_usable:int) :
        self.player_value = player_value
        self.dealer_card = dealer_card
        self.as_usable = as_usable

    def state_index(self):
        return Etat.calcul_index(self.player_value, self.dealer_card, self.as_usable)

    def calcul_index(player_value: int, dealer_card: int, as_usable:int):
        # Ramène la valeur du joueur à 0 à 10
        valeur_joueur = player_value - 12
        # Ramène la valeur du dealer à 0 à 10
        valeur_dealer = dealer_card - 12
        return valeur_joueur + valeur_dealer * 10 + 100* as_usable
        