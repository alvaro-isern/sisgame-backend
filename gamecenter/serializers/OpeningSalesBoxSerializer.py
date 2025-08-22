import rest_framework.serializers as serializers
from gamecenter.models import OpeningSalesBox

class OpeningSalesBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningSalesBox
        fields = '__all__'
