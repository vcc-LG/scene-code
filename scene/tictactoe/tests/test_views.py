from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Game, Move, Status
from django.urls import reverse
import numpy as np
import json

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

    def test_game_status_o_win_horz(self):
        self.client.post('/games/')
        game = Game.objects.last()
        move_1 = {'player': 'o', 'coords': '[0,1]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_1, format='json')
        move_2 = {'player': 'x', 'coords': '[0,0]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_2, format='json')
        move_3 = {'player': 'o', 'coords': '[1,1]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_3, format='json')
        move_4 = {'player': 'x', 'coords': '[1,0]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_4, format='json')
        move_5 = {'player': 'o', 'coords': '[2,1]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_5, format='json')
        game.refresh_from_db()
        self.assertEqual(game.status, Status.WIN)

    def test_game_status_x_win_vert(self):
        self.client.post('/games/')
        game = Game.objects.last()
        move_1 = {'player': 'x', 'coords': '[0,0]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_1, format='json')
        move_2 = {'player': 'o', 'coords': '[1,0]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_2, format='json')
        move_3 = {'player': 'x', 'coords': '[0,1]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_3, format='json')
        move_4 = {'player': 'o', 'coords': '[2,0]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_4, format='json')
        move_5 = {'player': 'x', 'coords': '[0,2]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_5, format='json')
        game.refresh_from_db()
        self.assertEqual(game.status, Status.WIN)
        
    def test_game_status_x_win_diag(self):
        self.client.post('/games/')
        game = Game.objects.last()
        move_1 = {'player': 'x', 'coords': '[0,0]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_1, format='json')
        move_2 = {'player': 'o', 'coords': '[1,0]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_2, format='json')
        move_3 = {'player': 'x', 'coords': '[1,1]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_3, format='json')
        move_4 = {'player': 'o', 'coords': '[2,0]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_4, format='json')
        move_5 = {'player': 'x', 'coords': '[2,2]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_5, format='json')
        game.refresh_from_db()
        self.assertEqual(game.status, Status.WIN)

    def test_game_status_x_win_antidiag(self):
        self.client.post('/games/')
        game = Game.objects.last()
        move_1 = {'player': 'x', 'coords': '[0,2]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_1, format='json')
        move_2 = {'player': 'o', 'coords': '[1,0]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_2, format='json')
        move_3 = {'player': 'x', 'coords': '[1,1]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_3, format='json')
        move_4 = {'player': 'o', 'coords': '[2,2]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_4, format='json')
        move_5 = {'player': 'x', 'coords': '[2,0]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_5, format='json')
        game.refresh_from_db()
        self.assertEqual(game.status, Status.WIN)

    def test_game_status_draw(self):
        self.client.post('/games/')
        game = Game.objects.last()
        move_1 = {'player': 'x', 'coords': '[0,0]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_1, format='json')
        move_2 = {'player': 'o', 'coords': '[1,0]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_2, format='json')
        move_3 = {'player': 'x', 'coords': '[2,0]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_3, format='json')
        move_4 = {'player': 'o', 'coords': '[1,1]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_4, format='json')
        move_5 = {'player': 'x', 'coords': '[0,1]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_5, format='json')
        move_6 = {'player': 'o', 'coords': '[2,1]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_6, format='json')      
        move_7 = {'player': 'x', 'coords': '[1,2]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_7, format='json')              
        move_8 = {'player': 'o', 'coords': '[0,2]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_8, format='json')     
        move_9 = {'player': 'x', 'coords': '[2,2]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': game.id}), move_9, format='json')                                
        game.refresh_from_db()
        self.assertEqual(game.status, Status.DRAW)        
        
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
        coords = [1, 1]
        data = {'player': 'o', 'coords': str(coords)}
        self.client.post(
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

    def test_post_moves_index_create_player_order_error(self):
        data = {'player': 'o', 'coords': '[1,1]'}
        self.client.post(
            reverse('moves-index', kwargs={'pk_game': self.game.id}), data, format='json')
        data = {'player': 'o', 'coords': '[1,2]'}
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
