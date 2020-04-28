import unittest
from etat import Etat
from episode import Game
class TestBlackJackMethods(unittest.TestCase):
    
    def test_index_etat(self):
        etat = Etat(10,5,1)
        index = etat.state_index();
        self.assertEqual(index, 160)

    def test_game_calculation(self):
        #usable as
        game = Game.calcul_value_player(10,1,0)
        self.assertEqual(game.sum,21)
        self.assertEqual(game.usable_as,1)
        #no usable as 
        game = Game.calcul_value_player(12,1,0)
        self.assertEqual(game.sum,13)
        self.assertEqual(game.usable_as,0)
        #use a previous as
        game = Game.calcul_value_player(15,7,1)
        self.assertEqual(game.sum,12)
        self.assertEqual(game.usable_as,0)
        

if __name__ == '__main__':
    unittest.main()