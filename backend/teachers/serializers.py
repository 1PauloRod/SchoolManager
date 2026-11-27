from rest_framework import serializers
from .models import Teacher
from django.db import transaction
from accounts.serializers import UserSerializer

class TeacherSerializer(serializers.ModelSerializer):
    
    name = serializers.CharField(source='teacher_id.name') 
    email = serializers.EmailField(source='teacher_id.email')
    cpf = serializers.CharField(source='teacher_id.cpf')
    role = serializers.CharField(source='teacher_id.role', read_only=True)
    active = serializers.BooleanField(source='teacher_id.is_active', read_only=True)
    
    class_name = serializers.CharField(source='class_id.name', read_only=True)
    
    class Meta:
        model = Teacher
        fields = [
                  'id', 
                  'name', 
                  'email', 
                  'cpf',
                  'role', 
                  'active', 
                  'specialty', 
                  'class_name', 
                  'status'
                  ]
        
    def get_fields(self):
        fields = super().get_fields()
        
        request = self.context.get("request")
        
        if request and request.method == 'POST':
            fields_post = [
                'name',
                'email',
                'cpf',
                'specialty'
            ]
            
            return {
                    name: field
                    for name, field in fields.items()
                    if name in fields_post
                    }
            
        return fields
    
    
    @transaction.atomic
    def create(self, validated_data):
        
        user_data = validated_data.pop("teacher_id", {})
        user_data.setdefault("role", "teacher")
        
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        return Teacher.objects.create(
            teacher_id = user, 
            **validated_data   
        )
        
    
    @transaction.atomic
    def update(self, instance, validated_data):
        
        user_data = validated_data.pop('teacher_id', {})
        user = instance.teacher_id
        
        if user_data:
            user_serializer = UserSerializer(
                                                instance=user, 
                                                data=user_data, 
                                                partial=True
                                                )
            user_serializer.is_valid(raise_exception=True) 
            user = user_serializer.save()
            
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance
        
        
        
        



