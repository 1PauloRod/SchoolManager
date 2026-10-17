from django.shortcuts import render
from .permissions import isAdmin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .service import getUser, deleteUser

#Quem vai fazer o cadastro do usuário vai ser o admin
class RegisterView(APIView):
    permission_classes = [AllowAny]
    #permission_classes = [isAdmin] faz mais sentido futuramente
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, 
                        status=status.HTTP_201_CREATED)
    

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        
        return Response(
            serializer.validated_data, 
            status=status.HTTP_200_OK
        )
        
class LogoutView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        request.auth.delete()
        
        return Response(
            {"message: Logout realizado com sucesso"}, 
              status=status.HTTP_200_OK          
              )
        
class getMeView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        user = UserSerializer(request.user)
        
        return Response(user.data, status=status.HTTP_200_OK)
        

#Paginar e cachear
class AccountsListView(APIView):
    
    permission_classes = [isAdmin]

    def get(self, request):
        #colocar exception bonitin
        users = User.objects.filter(is_superuser=False)
        
        serializer = UserSerializer(users, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AccountView(APIView):
    
    permission_classes = [isAdmin]
    
    def get(self, request, user_id):
        
        user = getUser(user_id) 
        
        serializer = UserSerializer(user)
        
        return Response(serializer.data, status.HTTP_200_OK)
    
    def put(self, request, user_id):
        pass
    
    def patch(self, request, user_id):
        
        user = getUser(user_id)

        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)   
        serializer.save()
        
        return Response({
            "message": f"Usuário {user.name} atualizado com sucesso.", 
            "user": serializer.data, 
        }, status=status.HTTP_200_OK)  
        
    
    def delete(self, request, user_id):
        
        user = deleteUser(user_id)
        
        return Response(
            {"message": f"usuário {user.name} deletado com sucesso."}, 
            status = status.HTTP_200_OK
                        )
        
        
        
        