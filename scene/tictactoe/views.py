from .models import Game, Move
from .serializers import GameSerializer, MoveSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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
/games/<pk_game>/moves/
'''


@api_view(['GET', 'POST'])
def move_list(request, pk_game):
    try:
        game = Game.objects.get(pk=pk_game)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        moves = Move.objects.filter(game__pk=pk_game).all()
        serializer = MoveSerializer(moves, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        data['game'] = pk_game
        serializer = MoveSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            game.update_grid()
            game.update_status()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def move_detail(request, pk_game, pk_move):
    try:
        Game.objects.get(pk=pk_game)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

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
