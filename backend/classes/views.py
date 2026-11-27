from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import isAdmin 
from .serializers import (ClassLevelSerializer, 
                        ClassSerializer, 
                        ClassSubjectSerializer,
                        ClassScheduleSerializer)
from rest_framework import status
from .models import Class, SchoolLevel, ClassSubject
from .service import (
                    getClass, 
                      deleteClass, 
                      getStudentsClass, 
                      getTeachersClass,
                      addStudentToClass,
                      deleteStudentClass, 
                      addTeacherToClass, 
                      deleteTeacherClass, 
                      getSchedules, 
                      addSchedule
                      )
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
    
    def post(self, request, class_id):
        
        student_id = request.data.get("student_id") 
        
        if not student_id:
            return Response({"error": "Informe o ID do aluno."}, 
                            status.HTTP_400_BAD_REQUEST)
            
        student = addStudentToClass(class_id, student_id)
        
        serializer = StudentSerializer(student)
        
        return Response(
            {
                "message": "Aluno adicionado à turma com sucesso.",
                "student": serializer.data
            },
            status=status.HTTP_200_OK
        )
        
    def delete(self, request, class_id):
        
        student_id = request.data.get("student_id")
        
        if not student_id:
            return Response({"error": "Informe o ID do aluno."}, 
                                        status.HTTP_400_BAD_REQUEST)
            
        
        deleteStudentClass(student_id, class_id)
        
        return Response(
                    {
                        "message": "Aluno excluido da turma com sucesso.",
                                        },
                    status=status.HTTP_200_OK
                )
           
class TeachersRegisterClassView(APIView):
    
    #permission_classes = [isAdmin]
    
    def get(self, request, class_id):
        
        teachers = getTeachersClass(class_id)
        serializer = TeacherSerializer(teachers, many=True)
        
        return Response(serializer.data, 
                                status=status.HTTP_200_OK) 
   
   
    def post(self, request, class_id):
       
        teacher_id = request.data.get("teacher_id") 


        if not teacher_id:
            return Response({"error": "Informe o ID do professor."}, 
                                       status.HTTP_400_BAD_REQUEST)
        
        teacher = addTeacherToClass(teacher_id, class_id)
        
        serializer = TeacherSerializer(teacher)
        
        return Response(
                    {
                        "message": "Professor adicionado à turma com sucesso.",
                        "teacher": serializer.data
                    },
                    status=status.HTTP_200_OK
                )
    
   
    def delete(self, request, class_id):
        
        teacher_id = request.data.get("teacher_id") 
        
        deleteTeacherClass(teacher_id)
        
        return Response(
                    {
                        "message": "Professor excluido da turma com sucesso.",
                                        },
                    status=status.HTTP_200_OK
                )
        

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
     
     

class ClassScheduleView(APIView):
    
    #permission_classes = [isAdmin]
    
    def get(self, request, class_id):
        
        schedules = getSchedules(class_id)
        
        serializer = ClassScheduleSerializer(
            schedules, 
            many=True
        )
        
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
        )
    
    def post(self, request, class_id):
        
        class_subject_id = request.data.get("class_subject")
        
        if not class_subject_id:
                    return Response(
                        {"error": "Informe a disciplina da turma."}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
        
        teacher_id = request.data.get("teacher_id") 
        
        if not teacher_id:
            return Response(
                {"error": "Informe o professor da aula."},
                status=status.HTTP_400_BAD_REQUEST
            )
                
        serializer = ClassScheduleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        
        schedules = addSchedule(class_id, teacher_id, class_subject_id, request.data)
        
        if not schedules:
            return Response(
                {"error": "Preencha os campos para criar a grade horária."}, 
                status=status.HTTP_400_BAD_REQUEST
            )    
        
        return Response(
            {
                "message": "Horário adicionado à grade com sucesso.",
                "schedule": ClassScheduleSerializer(schedules).data
            },
            status=status.HTTP_201_CREATED
        )
        
    def delete(self, request):
        pass