from django.urls import path 
from .views import EnrollmentsView, EnrollmentView
'''
urlpatterns = [
    path('', EnrollmentsView.as_view()), 
    path('<int:enrollment_id>/', EnrollmentView.as_view())
]'''