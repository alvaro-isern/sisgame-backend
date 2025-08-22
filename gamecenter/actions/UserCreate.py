from rest_framework.response import Response
from rest_framework import status
from gamecenter.models import User, Person
from gamecenter.serializers import CreateUserAccountSerializer

def user_create(request):
    """
    Función para crear un usuario con su persona asociada.
    """
    try:
        serializer = CreateUserAccountSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Error al enviar datos.', 
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar si ya existe un usuario con este email
        if User.objects.filter(email=serializer.validated_data.get('email')).exists():
            return Response({
                'message': 'Ya existe un usuario registrado con este email'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar si ya existe un usuario con este username
        if User.objects.filter(username=serializer.validated_data.get('username')).exists():
            return Response({
                'message': 'Ya existe un usuario registrado con este nombre de usuario'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Crear la persona
        person = Person.objects.create(
            name=serializer.validated_data.get('name'),
            phone=serializer.validated_data.get('phone', '')
        )
        
        # Crear el usuario asociado a la persona
        user = User.objects.create_user(
            username=serializer.validated_data.get('username'),
            email=serializer.validated_data.get('email'),
            password=serializer.validated_data.get('password'),
            person=person
        )

        return Response({
            'message': 'Usuario creado exitosamente.',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'person_name': person.name,
                'person_phone': person.phone
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'message': 'Ocurrió un error inesperado.',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
