from rest_framework.permissions import BasePermission

class isAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
    
class isTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.is_authenticated and request.user.role == 'teacher'
    
class isStudent(BasePermission):
    def has_permission(self, request, view):
        return request.is_authenticated and request.user.role == 'student'
 