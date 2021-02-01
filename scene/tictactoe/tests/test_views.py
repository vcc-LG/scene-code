import ipdb
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Game, Move
from django.urls import reverse
import numpy as np

class GameTests(APITestCase):
    def test_get_games_index_success(self):
        response = self.client.get(reverse('games-index'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_games_index_create(self):
        self.assertEqual(Game.objects.count(), 0)
        response = self.client.post(reverse('games-index'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.count(), 1)

    def test_get_games_detail_success(self):
        self.client.post('/games/')
        game = Game.objects.last()
        response = self.client.get(reverse('games-detail', args=(game.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_games_detail_not_found(self):
        response = self.client.get(reverse('games-detail', args=(999,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_game(self):
        self.client.post('/games/')
        game = Game.objects.last()
        response = self.client.delete(reverse('games-detail', args=(game.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_game_not_found(self):
        self.client.post('/games/')
        response = self.client.delete(reverse('games-detail', args=(999,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MoveTests(APITestCase):
    def setUp(self):
        self.client.post('/games/')
        self.game = Game.objects.last()

    def test_get_moves_index_success(self):
        response = self.client.get(
            reverse('moves-index', kwargs={'pk_game': self.game.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_moves_index_create(self):
        data = {'player': 'o', 'coords': '[1,1]'}
        response = self.client.post(
            reverse('moves-index', kwargs={'pk_game': self.game.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Move.objects.count(), 1)
        self.assertEqual(self.game.moves.count(), 1)

    def test_post_moves_index_updates_game_grid_array(self):
        coords = [1,1]
        data = {'player': 'o', 'coords': str(coords)}
        response = self.client.post(
            reverse('moves-index', kwargs={'pk_game': self.game.id}), data, format='json')
        self.game.refresh_from_db()
        self.assertEqual(np.where(self.game.grid_array == 'o')[0], coords[0])
        self.assertEqual(np.where(self.game.grid_array == 'o')[1], coords[1])

    def test_post_moves_index_create_illegal_coord_error(self):
        data = {'player': 'o', 'coords': '[4,4]'}
        response = self.client.post(
            reverse('moves-index', kwargs={'pk_game': self.game.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_moves_index_create_occupied_coord_error(self):
        data = {'player': 'o', 'coords': '[1,1]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': self.game.id}), data, format='json')
        data = {'player': 'x', 'coords': '[1,1]'}
        response = self.client.post(
            reverse('moves-index', kwargs={'pk_game': self.game.id}), data, format='json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_moves_detail_success(self):
        data = {'player': 'o', 'coords': '[1,1]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': self.game.id}), data, format='json')
        move = Move.objects.last()
        response = self.client.get(
            reverse('moves-detail', kwargs={'pk_game': self.game.id, 'pk_move': move.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_moves_detail_move_not_found(self):
        response = self.client.get(
            reverse('moves-detail', kwargs={'pk_game': self.game.id, 'pk_move': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_moves_detail_game_not_found(self):
        data = {'player': 'o', 'coords': '[1,1]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': self.game.id}), data, format='json')
        move = Move.objects.last()
        response = self.client.get(
            reverse('moves-detail', kwargs={'pk_game': 999, 'pk_move': move.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_move(self):
        data = {'player': 'o', 'coords': '[1,1]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': self.game.id}), data, format='json')
        move = Move.objects.last()
        response = self.client.delete(
            reverse('moves-detail', kwargs={'pk_game': self.game.id, 'pk_move': move.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_move_not_found(self):
        response = self.client.delete(
            reverse('moves-detail', kwargs={'pk_game': self.game.id, 'pk_move': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
