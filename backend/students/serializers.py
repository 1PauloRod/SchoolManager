from rest_framework import serializers
from .models import Student
from django.db import transaction
from accounts.serializers import UserSerializer


class StudentSerializer(serializers.ModelSerializer):
    
    name = serializers.CharField(source='student_id.name')
    email = serializers.EmailField(source='student_id.email')
    cpf = serializers.CharField(source='student_id.cpf')
    role = serializers.CharField(source='student_id.role', read_only=True)
    active = serializers.BooleanField(source='student_id.is_active')
    
    class_name = serializers.CharField(source='class_id.name', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id',
                  'name', 
                  'email',
                  'cpf',
                  'mother_name', 
                  'father_name',                 
                  'role',                               
                  'active',
                  'year',
                  'date_enrollment', 
                  'class_name', 
                  'status'
                  ]
        
    def get_fields(self):
        fields = super().get_fields() 
        
        request = self.context.get('request')
        
        if request and request.method == 'POST':
            fields_post = [
                'id',
                'name',
                'email',
                'cpf',
                'year',
                'mother_name',
                'father_name',
            ]
            
            return {
                name: field
                for name, field in fields.items()
                if name in fields_post
            }
            
        return fields 
    
    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop("student_id", {})
        user_data.setdefault("role", "student")

        print("DADOS DO USUÁRIO:", user_data)

        user_serializer = UserSerializer(data=user_data)

        print("CAMPOS DO SERIALIZER:", user_serializer.fields.keys())

        user_serializer.is_valid(raise_exception=True)

        user = user_serializer.save()

        return Student.objects.create(
            student_id=user,
            **validated_data
        )
        
        
    @transaction.atomic
    def update(self, instance, validated_data):
        # Extrai os campos que pertencem ao User
        user_data = validated_data.pop('student_id', {})
        user = instance.student_id

        # Atualiza o User através do UserSerializer
        if user_data:
            user_serializer = UserSerializer(
                instance=user,
                data=user_data,
                partial=True
            )
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        # Atualiza os campos do Student
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance




