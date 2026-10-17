from django.urls import path
from .views import (RegisterSchoolLevelView, 
                    ClassesView, 
                    ClassDetailView, 
                    StudentsRegisterClassView, 
                    TeachersRegisterClassView, 
                    SubjectsRegisterClassView
                    )

urlpatterns = [
    path('school-level/', RegisterSchoolLevelView.as_view()), 
    path('', ClassesView.as_view()), 
    path('<int:class_id>/', ClassDetailView.as_view()), 
    path('<int:class_id>/students/', StudentsRegisterClassView.as_view()), 
    path('<int:class_id>/teachers/', TeachersRegisterClassView.as_view()), 
    path('<int:class_id>/subjects/', SubjectsRegisterClassView.as_view())
]