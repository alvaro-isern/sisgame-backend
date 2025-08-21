from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from gamecenter.serializers import UserSerializer
from gamecenter.actions import *
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

   