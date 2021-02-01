import ipdb
from rest_framework import serializers
from .models import Game, Move, Players
import numpy as np
from .utils import empty_game_grid, coord_array_from_string


class GameSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    grid = serializers.CharField(read_only=True)
    moves = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        return Game.objects.create(**validated_data)

    class Meta:
        model = Game
        fields = ['id', 'status', 'grid', 'moves']


class MoveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    player = serializers.CharField(max_length=1)
    coords = serializers.CharField(max_length=20)
    game = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all())

    def create(self, validated_data):
        return Move.objects.create(**validated_data)

    def validate_coords(self, value):
        try:
            coords = coord_array_from_string(value)
        except:
            raise serializers.ValidationError("Could not parse coordinates")

        if not self.coords_legal(coords):
            raise serializers.ValidationError(
                "Coordinates are outside game grid")
        if not self.coords_unoccupied(coords):
            raise serializers.ValidationError("Coordinates are occupied")
        return value

    def coords_legal(self, coords):
        try:
            return True if not empty_game_grid()[coords[0]][coords[1]] else False
        except IndexError:
            return False

    def coords_unoccupied(self, coords):
        game = Game.objects.get(pk=self.initial_data['game'])
        return True if not game.grid_array[coords[0], coords[1]] else False

    class Meta:
        model = Move
        fields = ['id', 'player', 'coords', 'game']
