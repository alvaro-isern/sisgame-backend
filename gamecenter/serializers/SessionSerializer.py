from rest_framework import serializers
from gamecenter.models import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'