"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType


class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = UpdateGameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        games = Game.objects.all()

        game_type = request.query_params.get('type', None)

        if game_type:
            games = games.filter(game_type_id=game_type)

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests"""
        # Get the gamer based on the user that's logged in
        gamer = Gamer.objects.get(user=request.auth.user)

        # Get the GameType object from the game_type in the request body
        game_type = GameType.objects.get(pk=request.data['game_type'])

        # Inserting the new game into the database and added an id
        game = Game.objects.create(
            game_type=game_type,
            title=request.data['title'],
            maker=request.data['maker'],
            number_of_players=request.data['number_of_players'],
            skill_level=request.data['skill_level'],
            gamer=gamer
        )

        # Creating an instance of the serializer to be able to return json
        serializer = GameSerializer(game)

        # Returning the serialized data and 201 status code to the client
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """PUT update"""
        game = Game.objects.get(pk=pk)
        game.title = request.data['title']
        game.maker = request.data['maker']
        game.number_of_players = request.data['number_of_players']
        game.skill_level = request.data['skill_level']
        game.game_type = GameType.objects.get(pk=request.data['game_type'])
        game.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Delete game"""
        game = Game.objects.get(pk=pk)
        game.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game
        fields = '__all__'
        depth = 1


class UpdateGameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game
        fields = '__all__'
