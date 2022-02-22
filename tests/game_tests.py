from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from levelupapi.models import GameType, Game


class GameTests(APITestCase):
    def setUp(self):
        url = '/register'

        gamer = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }

        response = self.client.post(url, gamer, format='json')

        self.token = Token.objects.get(pk=response.data['token'])

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.game_type = GameType()
        self.game_type.label = "Board game"
        self.game_type.save()

        self.game = Game()
        self.game.gamer_id = 1
        self.game.title = "Sorry"
        self.game.maker = "Milton Bradley"
        self.game.skill_level = 5
        self.game.number_of_players = 4
        self.game.game_type_id = 1

        # Save the Game to the testing database
        self.game.save()

    def test_create_game(self):
        """Create game test"""
        url = "/games"

        # Define the Game properties
        game = {
            "title": "Clue",
            "maker": "Milton Bradley",
            "skill_level": 5,
            "number_of_players": 6,
            "game_type": 1,
        }

        response = self.client.post(url, game, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["gamer"]['user'], self.token.user_id)
        self.assertEqual(response.data["title"], game['title'])
        self.assertEqual(response.data["maker"], game['maker'])
        self.assertEqual(response.data["skill_level"], game['skill_level'])
        self.assertEqual(
            response.data["number_of_players"], game['number_of_players'])
        self.assertEqual(response.data["game_type"]['id'], game['game_type'])

    def test_get_game(self):
        """Get Game Test
        """
        game = Game()
        game.gamer_id = 1
        game.title = "Monopoly"
        game.maker = "Milton Bradley"
        game.skill_level = 5
        game.number_of_players = 4
        game.game_type_id = 1
        game.save()

        url = f'/games/{game.id}'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data["title"], game.title)
        self.assertEqual(response.data["maker"], game.maker)
        self.assertEqual(response.data["skill_level"], game.skill_level)
        self.assertEqual(
            response.data["number_of_players"], game.number_of_players)
        self.assertEqual(response.data["game_type"], game.game_type_id)

    def test_change_game(self):
        """test update game"""
        game = Game()
        game.game_type_id = self.game_type.id
        game.skill_level = 5
        game.title = "Sorry"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1

        # Save the Game to the testing database
        game.save()

        url = f'/games/{game.id}'

        new_game = {
            "title": "Sorry",
            "maker": "Hasbro",
            "skill_level": 2,
            "number_of_players": 4,
            "game_type": 1,
        }

        response = self.client.put(url, new_game, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data["gamer"], self.token.user_id)
        self.assertEqual(response.data["title"], new_game['title'])
        self.assertEqual(response.data["maker"], new_game['maker'])
        self.assertEqual(
            response.data["skill_level"], new_game['skill_level'])
        self.assertEqual(
            response.data["number_of_players"], new_game['number_of_players'])
        self.assertEqual(response.data["game_type"], new_game['game_type'])

    def test_delete_game(self):
        """Test delete game"""

        url = f'/games/{self.game.id}'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
