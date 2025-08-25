from rest_framework import viewsets
from gamecenter.models import User
from gamecenter.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

   