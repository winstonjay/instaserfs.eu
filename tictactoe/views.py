from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import F
from django.conf import settings

import json

from .models import Counter

from game import generate_response


def tic_tac_toe(request):
    """ Main View """
    count = Counter.objects.all()
    context = {
        "count": count,
        "google_analytics": settings.GOOGLE_ANALYTICS_PROPERTY_ID
    }
    return render(request, 'tictactoe/base.html', context)


def computer_move(request):
    """ respond with new move or if the game has finished """
    if request.method == 'POST':
        data = json.loads(request.body)
        board = data["gameBoard"]
        bot_player = data["botPlayer"]

        response_data = generate_response(board, bot_player)
        # RESPONSE KEYS: new_move, new_board, finished, winner, thoughts

        # count incrementer for winners
        if response_data["finished"]:
            winner = response_data["winner"]
            if winner == bot_player:
                index = 'computer'
            elif winner == None:
                index = 'draws'
            else:
                index = 'humans'
            counter = Counter.objects.get_or_create(title=index)[0]
            counter.count = F('count') + 1
            counter.save()

        return JsonResponse(response_data)

    return JsonResponse({"nout to see here": "this isnt happening"})
