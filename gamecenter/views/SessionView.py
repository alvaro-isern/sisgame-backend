from rest_framework import viewsets
from gamecenter.actions.sessions.DivicesList import get_devices_status_json
from gamecenter.models import Session
from gamecenter.serializers import SessionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    @action(detail=False, methods=['get'], url_path='devices-status')
    def get_devices_status(self, request):
        devices_status = get_devices_status_json()
        return Response(devices_status) 