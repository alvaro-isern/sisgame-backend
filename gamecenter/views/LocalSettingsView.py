from rest_framework import viewsets
from gamecenter.models import LocalSettings
from gamecenter.serializers import LocalSettingsSerializer

class LocalSettingsViewSet(viewsets.ModelViewSet):
    queryset = LocalSettings.objects.all()
    serializer_class = LocalSettingsSerializer
