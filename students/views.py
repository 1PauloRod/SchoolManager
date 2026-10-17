from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.permissions import isAdmin
from .serializers import StudentSerializer
from .models import Student
from .services import getStudent, deleteStudent

class StudentsView(APIView):
    
    permission_classes = [isAdmin]
    
    def get(self, request):
       
       students = Student.objects.all() 
       
       serializer = StudentSerializer(students, many=True)
       
       return Response(serializer.data, 
                       status=status.HTTP_200_OK)
   
    def post(self, request):
       
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        serializer.save()
       
        return Response(serializer.data, 
                        status=status.HTTP_201_CREATED)
   
   
class StudentView(APIView):
    
    permission_classes = [isAdmin]
    
    def get(self, request, student_id):
        
        student = getStudent(student_id)
        
        serializer = StudentSerializer(student)
        
        return Response(serializer.data, 
                        status=status.HTTP_200_OK)
    
    def delete(self, request, student_id):
        
        student = deleteStudent(student_id)
        
        return Response({"message": f"Estudante {student.user_id.name} deleteado com sucesso."}, 
                        status=status.HTTP_200_OK)
    
    def patch(self, request, student_id):
        
        student = getStudent(student_id)
        
        serializer = StudentSerializer(student, request.data, partial=True)
        serializer.is_valid(raise_exception=True) 
        serializer.save() 
        
        return Response({"message": f"Estudante {student.user_id.name} atualizado com sucesso."}, 
                        status=status.HTTP_200_OK)
        
        
    
    

