import rest_framework.serializers as serializers
from gamecenter.models import Person

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
