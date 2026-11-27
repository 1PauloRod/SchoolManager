from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), 
    path('classes/', include('classes.urls')), 
    path('subjects/', include('subjects.urls')), 
    #path('enrollments/', include('enrollments.urls')), 
    path('teachers/', include('teachers.urls')), 
    path('students/', include('students.urls'))
]
