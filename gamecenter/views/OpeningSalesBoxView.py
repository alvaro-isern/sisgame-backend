from rest_framework import viewsets
from gamecenter.models import OpeningSalesBox
from gamecenter.serializers import OpeningSalesBoxSerializer

class OpeningSalesBoxViewSet(viewsets.ModelViewSet):
    queryset = OpeningSalesBox.objects.all()
    serializer_class = OpeningSalesBoxSerializer
