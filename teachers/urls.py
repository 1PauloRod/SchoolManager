from django.urls import path
from .views import TeachersView, TeacherView

urlpatterns = [
    path('', TeachersView.as_view()), 
    path('<int:teacher_id>/', TeacherView.as_view())
]