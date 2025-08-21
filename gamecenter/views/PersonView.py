from rest_framework import viewsets
from gamecenter.models import Person
from gamecenter.serializers import PersonSerializer

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
