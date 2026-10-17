from rest_framework import serializers
from .models import Teacher

class TeacherSerializer(serializers.ModelSerializer):
    
    name = serializers.CharField(source='teacher_id.name') 
    email = serializers.EmailField(source='teacher_id.email')
    role = serializers.CharField(source='teacher_id.role')
    active = serializers.BooleanField(source='teacher_id.is_active')
    
    class_name = serializers.CharField(source='class_id.name')
    
    class Meta:
        model = Teacher
        fields = ['id', 
                  'name', 
                  'email', 
                  'role', 
                  'active', 
                  'specialty', 
                  'class_name']
        
        
        



