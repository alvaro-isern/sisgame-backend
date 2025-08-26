from rest_framework import viewsets
from gamecenter.models import Game
from gamecenter.serializers import GameSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer