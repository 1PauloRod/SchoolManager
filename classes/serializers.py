from rest_framework import serializers
from .models import Class, SchoolLevel
from .models import SchoolLevel, Class, ClassSubject


class ClassLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolLevel
        fields = "__all__"
        


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = "__all__" 
        

class ClassSubjectSerializer(serializers.ModelSerializer):
    
    class_name = serializers.CharField(source="class_id.name", read_only=True)
    subject_name = serializers.CharField(source="subject.name",  read_only=True)
    
    class Meta:
        model = ClassSubject
        fields = [
            'id', 
            'class_id', 
            'subject',
            'class_name', 
            'subject_name', 
            'weekday', 
            'start_time', 
            'end_time'
        ]