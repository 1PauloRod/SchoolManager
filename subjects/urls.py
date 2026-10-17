from django.urls import path
from .views import SubjectsView, SubjectView

urlpatterns = [
    path('', SubjectsView.as_view()), 
    path('<int:subject_id>/', SubjectView.as_view())
]