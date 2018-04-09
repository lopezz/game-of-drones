from django.db import models

class Game(models.Model):
    """The game model has variables to keep score and the winner"""
    player1 = models.CharField(max_length=255, blank=False)
    player2 = models.CharField(max_length=255, blank=False)
    player1_score = models.IntegerField(blank=True, null=False ,default=0)
    player2_score = models.IntegerField(blank=True, null=False ,default=0)
    winner = models.CharField(max_length=255, blank=True, null=True, default=None)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Overide the default save method check if the tow players are different"""
        
        if not self.pk and self.player1 == self.player2:
            raise ValueError('Two different players must be provied in order to create a game')
        return super(Game, self).save(*args, **kwargs)


def get_round_winner(p1_move, p2_move):
    """ Decides the winner of a round based on the rock-paper-scissors rules"""
    if(p1_move == p2_move):
        return 'draw'
    win_rules = {
        'rock': 'scissors',
        'paper': 'rock',
        'scissors': 'paper',
    }    
    return 'player1' if win_rules[p1_move] == p2_move else 'player2'

class GameRound(models.Model):
    """The GameRound model defines a game round with two player moves and a winner"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='rounds')
    player1_move = models.CharField(max_length=10, blank=False, null=False)
    player2_move = models.CharField(max_length=10, blank=False, null=False)
    # possible values for round_winner: 'player1', 'player2', 'draw'
    round_winner = models.CharField(max_length=255, blank=True, null=False)

    def save(self, *args, **kwargs):
        """when a round is performed, the moves are registered and the winner is decided before saving"""
        p1_move = self.player1_move
        p2_move = self.player2_move        
        winner = get_round_winner(p1_move, p2_move)
        self.round_winner = getattr(self.game, winner) if winner != 'draw' else winner
        return super(GameRound, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']

