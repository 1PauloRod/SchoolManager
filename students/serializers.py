from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    
    name = serializers.CharField(source='student_id.name')
    email = serializers.EmailField(source='student_id.email')
    role = serializers.CharField(source='student_id.role')
    active = serializers.BooleanField(source='student_id.is_active')
    
    class_name = serializers.CharField(source='class_id.name')
    
    class Meta:
        model = Student
        fields = ['id',
                  'name', 
                  'email',
                  'mother_name', 
                  'father_name', 
                  'role', 
                  'active',
                  'date_enrollment', 
                  'class_name'
                  ]