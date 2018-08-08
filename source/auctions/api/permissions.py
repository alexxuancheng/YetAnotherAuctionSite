from rest_framework import permissions

# SAFE_METHODS:GET','OPTIONS','HEAD'
class  CustomerAccessPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
        	return True
        elif request.method in ['PUT','PATCH'] and obj.seller != request.user:
        	return True
        elif request.method in ['DELETE'] and obj.seller == request.user:
        	return True
        # return obj.seller == request.user