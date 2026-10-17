from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import isAdmin 
from .serializers import ClassLevelSerializer, ClassSerializer, ClassSubjectSerializer
from rest_framework import status
from .models import Class, SchoolLevel, ClassSubject
from .service import (getClass, 
                      deleteClass, 
                      getStudentsClass, 
                      getTeachersClass)
#from accounts.serializers import UserSerializer
from students.serializers import StudentSerializer
from teachers.serializers import TeacherSerializer

class RegisterSchoolLevelView(APIView):
    
    #permission_classes = [isAdmin]
    
    def get(self, request):
        
        school_level = SchoolLevel.objects.all()
        
        serializer = ClassLevelSerializer(school_level, many=True)
        
        return Response(serializer.data, 
                        status=status.HTTP_200_OK
                        )
    
    
    def post(self, request):
        
        serializer = ClassLevelSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, 
                        status=status.HTTP_201_CREATED)
        

class ClassesView(APIView):
    
    '''def has_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        
        return [isAdmin()]'''
    
    def get(self, request):
        
        classes = Class.objects.all()
        serializer = ClassSerializer(classes, many=True)
        
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
        
    
    def post(self, request): #create Class
        
        serializer = ClassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, 
                        status=status.HTTP_201_CREATED)
        
    
class ClassDetailView(APIView):
    
    #permission_classes = [isAdmin]
    
    def get(self, request, class_id):
        
        class_details = getClass(class_id)
        
        serializer = ClassSerializer(class_details)
        
        return Response(serializer.data, 
                        status=status.HTTP_200_OK)
         
        
    def patch(self, request, class_id):
        
        class_detail = getClass(class_id)
        serializer = ClassSerializer(class_detail, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
                    "message": f"Turma {class_detail.name} atualizado com sucesso.", 
                    "class": serializer.data, 
                }, status=status.HTTP_200_OK)  
    
    def delete(self, request, class_id):
        
        class_detail = deleteClass(class_id)
        
        return Response(
                    {"message": f"Turma {class_detail.name} deletado com sucesso."}, 
                    status = status.HTTP_200_OK
                                )

    
class StudentsRegisterClassView(APIView):
    
    #permission_classes = [isAdmin]
    
    def get(self, request, class_id):
        
        students = getStudentsClass(class_id) 
        
        serializer = StudentSerializer(students, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK) 

class TeachersRegisterClassView(APIView):
    
    #permission_classes = [isAdmin]
    
    def get(self, request, class_id):
        
        teachers = getTeachersClass(class_id)
        serializer = TeacherSerializer(teachers, many=True)
        
        return Response(serializer.data, 
                                status=status.HTTP_200_OK) 
    

class SubjectsRegisterClassView(APIView):
    
    #permission_classes = [isAdmin]
    
    def get(self, request, class_id):
        
        class_details = getClass(class_id) 
        
        class_subjects = ClassSubject.objects.filter(
            class_id=class_details
        ).select_related("subject")
        
        serializer = ClassSubjectSerializer(class_subjects, many=True)
        
        return Response(serializer.data, 
                        status=status.HTTP_200_OK)
    
    def post(self, request, class_id):
        
        class_details = getClass(class_id)
        
        serializer = ClassSubjectSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True) 
        serializer.save(class_id=class_details) 
        
        return Response(serializer.data, 
                        status=status.HTTP_201_CREATED)
     