from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from http import HTTPStatus
from .models import Game, GameRound

import json

WIN_SCORE = 3    #This variable defines the score needed to win a game

@csrf_exempt
def create_game(request):
    """This view defines the create behavior for games in the api."""  
    if request.method != 'POST':
        return JsonResponse({'status':'error', 'error_msg': 'Only POST requests allowed'})
    player1_name = request.POST.get('player1')
    player2_name = request.POST.get('player2')
    print(request.POST)
    try:
        new_game = Game(player1=player1_name, player2=player2_name)    
        new_game.save()
    except ValueError as e:
        print(str(e))
        return JsonResponse({'status':'error', 'error_msg': str(e)})
    data = {
        'game_id': new_game.pk,
    }
    response = JsonResponse(data)
    response.status_code = HTTPStatus.CREATED        
    return response
    
def get_score(request):
    """This view returns the score data for a given game. """
    if request.method != 'GET':
        return JsonResponse({'status':'error', 'error_msg': 'Only GET requests allowed'})
    game_id = request.GET.get('game_id')
    try:
        game = Game.objects.get(pk=game_id)
    except ObjectDoesNotExist:
        return JsonResponse({'status':'error', 'error_msg': 'The game with id={} does not exists'.format(game_id)})
    else:
        game_rounds = game.rounds.all()
        # set the game rounds list        
        game_rounds = [{'round_no':n+1, 'round_winner': _round.round_winner} for n, _round in enumerate(game_rounds)]
        data = {
            'game_id': game.pk,
            'player1_score': game.player1_score,
            'player2_score': game.player2_score,
            'game_rounds': game_rounds
        }
    return JsonResponse(data)


@csrf_exempt
def register_round(request):
    """This view defines the create behavior for game rounds in the api. """
    if request.method != 'POST':
        return JsonResponse({'status':'error', 'error_msg': 'Only POST requests allowed'})
    game_id = request.POST.get('game_id')

    try:
        game = Game.objects.get(pk=game_id)
    except ObjectDoesNotExist:
        return JsonResponse({'status':'error', 'error_msg': 'The game with id={} does not exists'.format(game_id)})
    else:
        player1_move = request.POST.get('player1_move')
        player2_move = request.POST.get('player2_move')
        game_round = GameRound(game=game,player1_move=player1_move, player2_move=player2_move)
        game_round.save()

        update_score(game, game_round.round_winner)            

        response = JsonResponse({'success': True, 'winner':game.winner})
        response.status_code = HTTPStatus.CREATED
        return response

def update_score(game, winner):
    player1 = game.player1
    player2 = game.player2
    if(player1 == winner):        
        game.player1_score +=1
        winner_score = game.player1_score
    elif(player2 == winner):
        game.player2_score +=1
        winner_score = game.player2_score
    else:
        # there was a draw
        return False
    if winner_score == WIN_SCORE:
        game.winner = winner
    game.save()
    return True

def get_game_history(request):
    """Returns the list of all games played to date"""
    pass

def get_ranking(request):
    """Returns a list of players ranked by the number of games won"""
    pass

