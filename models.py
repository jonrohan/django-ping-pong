import datetime

from django.contrib.sites.models import Site
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group
from django.db.models import Q
from django.db import models

class Employee(models.Model):
    user = models.OneToOneField(DjangoUser,limit_choices_to={'is_staff': True},help_text="Only is_staff django users in this list")
    
    twitter = models.URLField(blank=True,verify_exists=False,help_text="ie. http://twitter.com/mg")
    
    facebook = models.URLField(blank=True,verify_exists=False,help_text="ie. http://facebook.com/mg")
    
    website = models.URLField(blank=True,verify_exists=False)
    
    skype = models.CharField(max_length=100,blank=True)

    aim = models.CharField(max_length=100,blank=True)

    title = models.CharField(max_length=100)

    nick_name = models.CharField(max_length=100,blank=True,default="")
    
    bio = models.TextField(blank=True)
    
    teams = models.ManyToManyField(Group)
    
    birthday = models.DateField(blank=True, null=True)

    date_joined = models.DateTimeField()
    
    def __unicode__(self):
        return unicode(self.user)

    def is_new(self):
        return (datetime.datetime.now() - self.date_joined) < datetime.timedelta(90)
        
    def is_birthday(self):
        if not self.birthday:
            return False
        today = datetime.datetime.utcnow()
        
        return today.day == self.birthday.day and today.month == self.birthday.month

    def full_name(self):
        return unicode(self.user.first_name + " " + self.user.last_name)
        
    def is_social(self):
        return (self.twitter or self.facebook or self.website or self.skype or self.aim)

class PingPongMatch(models.Model):
    
    player_1 = models.ForeignKey(Employee,related_name="player_1")
    
    player_2 = models.ForeignKey(Employee,related_name="player_2")

    date = models.DateTimeField(auto_now_add=True)
    
    def winner(self):
        
        player1_games = 0
        player2_games = 0
        
        games = PingPongGame.objects.filter(match=self)
        for game in games:
            if game.player1_points > game.player2_points:
                player1_games = player1_games + 1
            else:
                player2_games = player2_games + 1
        
        if player1_games > player2_games:
            return self.player_1
            
        return self.player_2
        
    
    def __unicode__(self):
        return '%s vs. %s' % (self.player_1.full_name(),
                            self.player_2.full_name())

class PingPongGame(models.Model):
    
    player1_points = models.IntegerField(default=0)

    player2_points = models.IntegerField(default=0)
    match = models.ForeignKey(PingPongMatch, related_name='games')

    def save(self, *args, **kwargs):
        """
        We want to add to PingPongRecords everytime a game is saved.
        """
        super(PingPongGame, self).save(*args, **kwargs)
        player_1_record, status = PingPongRecords.objects.get_or_create(player=self.match.player_1)
        player_2_record, status = PingPongRecords.objects.get_or_create(player=self.match.player_2)
        if int(self.player1_points) > int(self.player2_points):
            player_1_record.game_wins = player_1_record.game_wins + 1 if player_1_record.game_wins else 1
            player_2_record.game_losses = player_2_record.game_losses + 1 if player_2_record.game_losses else 1
        else:
            player_2_record.game_wins = player_2_record.game_wins + 1 if player_2_record.game_wins else 1
            player_1_record.game_losses = player_1_record.game_losses + 1 if player_1_record.game_losses else 1
        player_1_record.games_played = player_1_record.games_played + 1
        player_2_record.games_played = player_2_record.games_played + 1
        player_1_record.matches.add(self.match)
        player_2_record.matches.add(self.match)
        player_1_record.save()
        player_2_record.save()
    
    def __unicode__(self):
        return '%s, %s' % (self.player1_points, self.player2_points)
    
class PingPongRecords(models.Model):
    player = models.ForeignKey(Employee)
    game_wins = models.IntegerField(default=0, blank=True, null=True)
    game_losses = models.IntegerField(default=0, blank=True, null=True)
    match_wins = models.IntegerField(default=0, blank=True, null=True)
    match_losses = models.IntegerField(default=0, blank=True, null=True)
    games_played = models.IntegerField(default=0, blank=True, null=True)
    win_ratio = models.FloatField(default=0.00, blank=True, null=True)
    matches = models.ManyToManyField(PingPongMatch)
    
    def __unicode__(self):
        return '%s' % self.player.user.username
