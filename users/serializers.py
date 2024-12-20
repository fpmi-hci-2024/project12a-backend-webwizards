from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        print(f"Attempting login with username: {username} and password: {password}")  # Debugging line

        # Authenticate using the username and password
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('Неверные учетные данные.')

        attrs['user'] = user
        return attrs