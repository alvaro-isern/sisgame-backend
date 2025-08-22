import rest_framework.serializers as serializers
from gamecenter.models import User

class CreateUserAccountSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    name = serializers.CharField()
    phone = serializers.CharField()

    def validate_email(self, value):
        """Validar que el email no esté ya registrado"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe un usuario registrado con este email")
        return value
    
    def validate_username(self, value):
        """Validar que el username no esté ya registrado"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ya existe un usuario registrado con este nombre de usuario")
        return value

    def validate_password(self, value):
        """Validar la fortaleza de la contraseña"""
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres")
        return value
