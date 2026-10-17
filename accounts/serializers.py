from rest_framework import serializers
from .models import User
from .exceptions import EmailAlreadyExistsError, CPFAlreadyExistsError, PasswordDistinctError, InvalidCredentialsError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
                    "id", 
                    "name",
                    "email",
                    "cpf",
                    "birthday",
                    "role",
                    "is_active"
                ]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[])
    cpf = serializers.CharField(validators=[])
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id", 
            "name",
            "email",
            "cpf",
            "birthday",
            "role",
            "is_active",
            "password",
            "password2",
        ]

    #colocar as outras validacoes
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise EmailAlreadyExistsError()
        return value
    
    def validate_cpf(self, value):
        if User.objects.filter(cpf=value).exists():
            raise CPFAlreadyExistsError()
        
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise PasswordDistinctError()
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(
            **validated_data
        )

        return user


class LoginSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except Exception:
            raise InvalidCredentialsError()
        