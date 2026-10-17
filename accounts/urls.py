from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    LogoutView, 
    getMeView,
    AccountsListView, 
    AccountView, 
    
    )
from rest_framework_simplejwt.views import (
    #TokenObtainPairView, chamado agora no serializer 
    TokenRefreshView
)

urlpatterns = [
    path("register/", RegisterView.as_view()), 
    path("login/", LoginView.as_view()), 
    path("me/", getMeView.as_view()),
    path("usersList/", AccountsListView.as_view()),
    path("<int:user_id>/", AccountView.as_view()), 
    path("logout/", LogoutView.as_view()), 
    path("refresh/", TokenRefreshView.as_view())
]