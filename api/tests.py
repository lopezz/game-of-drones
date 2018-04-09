from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus
from .models import Game, GameRound, get_round_winner

import json


# Known round winners for any p1 and p2 moves.
KNOWN_ROUND_RESULTS = (
    (('paper','paper'),'draw'),
    (('paper','rock'),'player1'),
    (('paper','scissors'),'player2'),
    (('rock','rock'),'draw'),
    (('rock','paper'),'player2'),
    (('rock','scissors'),'player1'),    
    (('scissors','scissors'),'draw'),
    (('scissors','rock'),'player2'),
    (('scissors','paper'),'player1'),
)

class ModelTestCase(TestCase):
    """This class defines the test suite for the game model."""

    def setUp(self):
        """Define test variables."""
        self.player1_name = 'pepito'
        self.player2_name = 'juanito'
        self.old_games_count = Game.objects.count()
        self.game = Game(player1=self.player1_name, player2=self.player2_name)
        self.game.save()

    def test_model_can_create_a_game(self):
        """Test the game model can create a game."""
        new_count = Game.objects.count()
        self.assertNotEqual(self.old_games_count, new_count)

    def test_model_game_same_name_constraint(self):
        """Test the game model raises ValueException if the two players have the same name"""
        game = Game(player1=self.player1_name, player2=self.player1_name)
        self.assertRaises(ValueError, game.save)

    def test_model_can_create_a_game_round(self):
        """Test the gameRound model can create a game round."""        
        game_round = GameRound(game=self.game, player1_move='rock', player2_move='scissors')
        old_count = GameRound.objects.count()
        game_round.save()
        new_count = GameRound.objects.count()
        self.assertNotEqual(old_count, new_count)
    
    def test_model_correctly_chooses_winner(self):
        """Test the game round model correctly chooses a winner."""
        game_round = GameRound.objects.create(game=self.game, player1_move='rock', player2_move='scissors')        
        self.assertEqual(game_round.round_winner, self.player1_name)

    def test_model_known_round_results(self):
        """Test the rules of rock-paper-scissors implemented in get_round_winner"""
        for moves, winner in KNOWN_ROUND_RESULTS:
            round_winner = get_round_winner(*moves)
            self.assertEqual(round_winner, winner)

class ViewsTestCase(TestCase):
    """Test suite for the api views."""
    
    def setUp(self):
        """Define the test client and other test variables"""
        self.client = Client()
        self.player1_name = 'fulanito'
        self.player2_name = 'ramoncito'
        game_data = {
            'player1':self.player1_name,
            'player2':self.player2_name,
        }
        self.response = self.client.post(reverse('create_game'), game_data, format='json')

    def test_api_can_create_a_game(self):
        """Test the api has game creation capacity"""
        self.assertEqual(self.response.status_code, HTTPStatus.CREATED)
        
    def test_api_can_retrieve_a_game_score(self):
        """Test the api can get a game score"""        
        game = Game.objects.create(player1=self.player1_name, player2=self.player2_name)
        GameRound.objects.create(game=game, player1_move='rock', player2_move='scissors')
        GameRound.objects.create(game=game, player1_move='rock', player2_move='rock')
        GameRound.objects.create(game=game, player1_move='paper', player2_move='scissors')
        request_url = reverse('get_score')+'?game_id={}'.format(game.pk)
        response = self.client.get(request_url)
        print(response.content.decode('utf-8'))
        # self.assertEqual(response)

    def test_api_can_register_a_game_round(self):
        """Test the api can register a game round"""
        game = Game.objects.create(player1=self.player1_name, player2=self.player2_name)
        round_data = {
            'game_id': game.pk,
            'player1_move': 'scissors',
            'player2_move': 'rock'
        }
        response = self.client.post(reverse('register_round'), round_data, format='json')
        print(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_api_can_choose_a_winner(self):
        """Test the api return a winner if there is one"""        
        game = Game.objects.create(player1=self.player1_name, player2=self.player2_name, player1_score=2)
        round_data = {
            'game_id': game.pk,
            'player1_move': 'rock',
            'player2_move': 'scissors'
        }
        response = self.client.post(reverse('register_round'), round_data, format='json')
        winner = json.loads(response.content.decode('utf-8'))['winner']
        self.assertEqual(winner, self.player1_name)
        