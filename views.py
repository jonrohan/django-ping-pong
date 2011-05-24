from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden

from models import *
from const import PING_PONG_BEST_OF

@staff_member_required
def new_match(request):
    
    if request.method == "POST":
        player1 = Employee.objects.get(id=request.POST.get("player_1",""))
        player2 = Employee.objects.get(id=request.POST.get("player_2",""))
        if player1 != player2:
            match = PingPongMatch(player_1=player1,player_2=player2)
            match.save()
            player1_games = 0
            player2_games = 0
            for i in [1,2,3]:
                score1 = request.POST.get("player1_game%i"%i,None)
                score2 = request.POST.get("player2_game%i"%i,None)
                if score1 and score2:
                    if int(score1) > int(score2):
                        player1_games = player1_games + 1
                    else:
                        player2_games = player2_games + 1
                    game = PingPongGame(player1_points=score1,player2_points=score2,match=match)
                    game.save()
                    
            player_1_record = PingPongRecords.objects.get(player=player1)
            player_2_record = PingPongRecords.objects.get(player=player2)
            if player1_games > player2_games:
                player_1_record.match_wins = player_1_record.match_wins + 1
                player_1_record.save()
            else:
                player_2_record.match_wins = player_2_record.match_wins + 1
                player_2_record.save()
            player_1_record.win_ratio = round((float(player_1_record.game_wins) / float(player_1_record.games_played)) * 100, 2)
            player_2_record.win_ratio = round((float(player_2_record.game_wins) / float(player_2_record.games_played)) * 100, 2)
            player_1_record.save()
            player_2_record.save()
            return HttpResponseRedirect(reverse("pingpong_match",kwargs={"match_id":match.id}))
    employees = Employee.objects.all()
    
    return render_to_response('employees/new_pingpong.html', 
        {
            "employees":employees,
            "num_games":PING_PONG_BEST_OF
        }, 
        context_instance=RequestContext(request))

@staff_member_required
def match(request,match_id):
    
    match = get_object_or_404(PingPongMatch,id=match_id)
    
    return render_to_response('employees/pingpong_match.html', 
        {
            "match":match,
            
        }, 
        context_instance=RequestContext(request))


@staff_member_required
def pingpong(request):

    records = PingPongRecords.objects.all().order_by("game_wins").reverse()
    
    return render_to_response('employees/pingpong_leaderboard.html', 
        {
            "records":records
        }, 
        context_instance=RequestContext(request))
