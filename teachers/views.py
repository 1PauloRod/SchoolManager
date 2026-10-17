from rest_framework.response import Response 
from rest_framework.views import APIView
from accounts.permissions import isAdmin
from .serializers import TeacherSerializer
from rest_framework import status
from .models import Teacher
from .services import getTeacher, deleteTeacher

class TeachersView(APIView):
    
    permission_classes = [isAdmin]
    
    def get(self, request):
        
        teachers = Teacher.objects.all()
        
        serializer = TeacherSerializer(teachers, many=True)
        
        return Response(serializer.data, 
                        status=status.HTTP_200_OK)
        
    def post(self, request):
        
        serializer = TeacherSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, 
                        status=status.HTTP_201_CREATED)
        

class TeacherView(APIView):
    
    permission_classes = [isAdmin]
    
    def get(self, request, teacher_id):
        
        teacher = getTeacher(teacher_id)
        
        serializer = TeacherSerializer(teacher)
        
        return Response(serializer.data, 
                        status=status.HTTP_200_OK)
        
    
    def delete(self, request, teacher_id):
        
        teacher = deleteTeacher(teacher_id)
        
        return Response(
            {"message": f"Professor {teacher.teacher_id.name} deletado com sucesso."},
            status=status.HTTP_200_OK 
            
        )
    
    def patch(self, request, teacher_id):
        
        teacher = getTeacher(teacher_id)
        
        serializer = TeacherSerializer(teacher, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            {"message:" f"Professor {teacher.teacher_id.name} atualizado com sucesso."}, 
            status=status.HTTP_200_OK
        )
    