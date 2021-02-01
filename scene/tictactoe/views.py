from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import ipdb
from rest_framework.parsers import JSONParser
from .models import Game, Move, Players
from .serializers import GameSerializer, MoveSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import numpy as np

'''
/games/
'''


@api_view(['GET', 'POST'])
def game_list(request):
    if request.method == 'GET':
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def game_detail(request, pk_game):
    try:
        game = Game.objects.get(pk=pk_game)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GameSerializer(game)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''
/games/<pk>/moves/
'''


@api_view(['GET', 'POST'])
def move_list(request, pk_game):
    if request.method == 'GET':
        moves = Move.objects.filter(game__pk=pk_game).all()
        serializer = MoveSerializer(moves, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # try:
        #     game = Game.objects.get(pk=pk_game)
        # except Game.DoesNotExist:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        data['game'] = pk_game
        serializer = MoveSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def move_detail(request, pk_game, pk_move):
    try:
        move = Move.objects.get(pk=pk_move)
    except Move.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MoveSerializer(move)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        move.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def player_from_string(player_string):
    if player_string == 'x':
        return Players.CROSSES
    elif player_string == 'o':
        return Players.NOUGHTS
    else:
        return None
