import rest_framework.serializers as serializers
from gamecenter.models import Person
from django.contrib.auth.models import User
from gamecenter.serializers import PersonSerializer

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)    
    person = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'person']
        read_only_fields = ['id']

    def create(self, validated_data):
        # Remove the person field from validated_data since User model doesn't have it
        person = validated_data.pop('person', None)
        
        # Initialize user data with defaults
        user_data = {
            'username': validated_data['username'],
            'password': validated_data['password'],
            'first_name': '',
            'last_name': '',
            'email': ''
        }
        
        # If a person is provided, use their data for the user fields
        if person:
            # Override user fields with person data if person has those fields
            if person.first_name:
                user_data['first_name'] = person.first_name
            if person.last_name:
                user_data['last_name'] = person.last_name
            if person.email:
                user_data['email'] = person.email
        
        # Create the user with the data (either defaults or person data)
        user = User.objects.create_user(
            username=user_data['username'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email']
        )
        
        # If a person was provided, associate it with the user
        if person:
            person.user = user
            person.save()
            
        return user

    def update(self, instance, validated_data):
        # Remove the person field from validated_data
        person = validated_data.pop('person', None)
        
        # Update user fields
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        
        # Update person association if provided
        if person is not None:
            # First, remove any existing association
            try:
                existing_person = Person.objects.get(user=instance)
                existing_person.user = None
                existing_person.save()
            except Person.DoesNotExist:
                pass
            
            # Then set the new association and sync data
            if person:
                person.user = instance
                person.save()
                
                # Sync person data to user fields
                if person.first_name:
                    instance.first_name = person.first_name
                if person.last_name:
                    instance.last_name = person.last_name
                if person.email:
                    instance.email = person.email
                instance.save()
                
        return instance

    def to_representation(self, instance):
        # Get the default representation
        representation = super().to_representation(instance)
        
        # Add the person data
        try:
            person = Person.objects.get(user=instance)
            representation['person'] = PersonSerializer(person).data
        except Person.DoesNotExist:
            representation['person'] = None
            
        return representation
