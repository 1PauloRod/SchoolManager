from rest_framework import serializers
from .models import User
from .exceptions import EmailAlreadyExistsError, CPFAlreadyExistsError, PasswordDistinctError, InvalidCredentialsError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(
        required=False,
        default='student'
    )
    
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
            "is_active"
        ]

    #colocar as outras validacoes
    def validate_email(self, value):
        queryset = User.objects.filter(email=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise EmailAlreadyExistsError()

        return value
    
    def validate_cpf(self, value):
        if User.objects.filter(cpf=value).exists():
            raise CPFAlreadyExistsError()
        
        #colocar para validar o formato do cpf tambem
        
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise PasswordDistinctError()
        return attrs

    def create(self, validated_data):
        password = validated_data["cpf"] + validated_data["name"]
        user = User.objects.create_user(
            password = password,
            **validated_data
        )

        return user


class LoginSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except Exception:
            raise InvalidCredentialsError()
        