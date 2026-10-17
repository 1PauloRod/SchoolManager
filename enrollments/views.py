from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EnrollmentSerializer
from .models import Enrollment 
from accounts.permissions import isStudent, isAdmin
from .services import getEnrollment, deleteEnrollment
'''
class EnrollmentsView(APIView):
    
    permission_classes = [isAdmin]
    
    def get(self, request):
        
        enrollments = Enrollment.objects.all()
        
        serializer = EnrollmentSerializer(enrollments, many=True)

        return Response(serializer.data, 
                        status=status.HTTP_200_OK)
        
    
    def post(self, request):
        
        serializer = EnrollmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        
        return Response(serializer.data, 
                        status=status.HTTP_201_CREATED)
        

class EnrollmentView(APIView):
    
    def has_permission(self, request):
        
        if request.method == 'GET':
            return [isAdmin(), isStudent()]
        
        return [isAdmin()]
    
    def get(self, request, enrollment_id):
        
        enrollment = getEnrollment(enrollment_id)
        
        serializer = EnrollmentSerializer(enrollment)
        
        return Response(serializer.data, 
                        status=status.HTTP_200_OK)
    
    
    def delete(self, request, enrollment_id):
        
        enrollment = deleteEnrollment(enrollment_id)
        
        return Response(
                    {"message": f"Matrícula {enrollment.student_id.name} deletada com sucesso."}, 
                    status = status.HTTP_200_OK
                                )
        
    
    def patch(self, request, enrollment_id):
        
        enrollment = getEnrollment(enrollment_id)
        
        serializer = EnrollmentSerializer(enrollment, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
                            {"message": f"Matrícula {enrollment.student_id.name} atualizada com sucesso."}, 
                            status = status.HTTP_200_OK
                        )'''