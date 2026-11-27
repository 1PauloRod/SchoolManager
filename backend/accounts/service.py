from .models import User
from .exceptions import UserNotFoundError

def getUser(user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise UserNotFoundError()
    
    return user

def deleteUser(user_id):
    try:
        user = User.objects.get(id=user_id) 
    except User.DoesNotExist:
        raise UserNotFoundError()
    
    user.delete()
    
    return user
        
    
    
    