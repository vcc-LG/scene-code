import ipdb
from rest_framework import serializers
from .models import Game, Move, Players
import numpy as np

# def validate(self, data):
#     if data['start'] > data['finish']:
#         raise serializers.ValidationError("finish must occur after start")
#     return data


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
    coords = serializers.CharField(max_length=5)
    game = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all())

    def create(self, validated_data):
        return Move.objects.create(**validated_data)

    class Meta:
        model = Move
        fields = ['id', 'player', 'coords', 'game']
