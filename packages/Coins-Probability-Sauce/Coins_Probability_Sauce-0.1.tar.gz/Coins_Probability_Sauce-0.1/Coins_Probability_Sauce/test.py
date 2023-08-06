import unittest
from Coins_Probability_Sauce import Bayes_Coins


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.collection = Bayes_Coins(A_prob=.8, B_prob=.4)
        self.collection.create_new_collection(As=50, Bs=25, A_prob=.2, B_prob=.7)

    def test_initialization(self):
        self.assertEqual(self.collection.A_prob, .2, 'Incorrect A_prob')
        self.assertEqual(self.collection.B_prob, .7, 'Incorrect B_prob')
        self.assertEqual(self.collection.A_count, 50, 'Incorrect A count')
        self.assertEqual(self.collection.B_count, 25, 'Incorrect B count')

    def test_calculate_coin_counts(self):
        self.assertEqual(self.collection.calculate_A_coins(), 50, 'Calculate A coins not as expected.')
        self.assertEqual(self.collection.calculate_B_coins(), 25, 'Calculate B coins not as expected.')

    def test_both_coins_heads(self):
        self.assertEqual(self.collection.heads_from_both_coins(), .14, 'Both coins heads calculation not as expected.')

    def test_random_flips(self):
        self.assertEqual(self.collection.calculate_random_flip_heads(), .37, 'Random flip heads calculation not as '
                                                                             'expected.')
        self.assertEqual(self.collection.calculate_random_flip_tails(), .63, 'Random flip tails calculation not as '
                                                                             'expected.')


if __name__ == '__main__':
    unittest.main()
