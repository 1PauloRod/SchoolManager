from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import isAdmin
from .models import Subject
from .serializers import SubjectsSerializer
from rest_framework.response import Response
from rest_framework import status
from .services import getSubject, deleteSubject

class SubjectsView(APIView):
    
    '''def has_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        
        return [isAdmin()]'''
    
    def get(self, request):

        subjects = Subject.objects.all()
        
        serializer = SubjectsSerializer(subjects, many=True)
        
        return Response(serializer.data, 
                        status=status.HTTP_200_OK)
        
    
    def post(self, request):
        
        serializer = SubjectsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, 
                        status=status.HTTP_201_CREATED
                        )
        
        
class SubjectView(APIView):
    
    #permission_classes = [isAdmin]
    
    def get(self, request, subject_id):
        
        subject = getSubject(subject_id)
        
        serializer = SubjectsSerializer(subject)
        
        return Response(serializer.data, 
                        status=status.HTTP_200_OK)

            
    def delete(self, request, subject_id):
        
        subject = deleteSubject(subject_id)
        
        serializer = SubjectsSerializer(subject)
        
        return Response(
                            {"message": f"Matéria {subject.name} deletado com sucesso."}, 
                            status = status.HTTP_200_OK
                                        )
    
    def patch(self, request, subject_id):
        
        subject = getSubject(subject_id)
        
        serializer = SubjectsSerializer(subject, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        
        return Response({
                            "message": f"Turma {subject.name} atualizado com sucesso.", 
                            "class": serializer.data, 
                        }, status=status.HTTP_200_OK)  
        
        
        
        