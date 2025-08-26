from rest_framework import viewsets
from gamecenter.models import Session
from gamecenter.serializers import SessionSerializer

class SessionsViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer