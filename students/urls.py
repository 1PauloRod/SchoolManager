from django.urls import path 
from .views import StudentsView, StudentView

urlpatterns = [
    path('', StudentsView.as_view()), 
    path('<int:student_id>/', StudentView.as_view())
]
