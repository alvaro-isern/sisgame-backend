from  rest_framework import viewsets
from gamecenter.models import ProductGame
from gamecenter.serializers import ProductGameSerializer

class ProductGameViewSet(viewsets.ModelViewSet):
    queryset = ProductGame.objects.all()
    serializer_class = ProductGameSerializer
