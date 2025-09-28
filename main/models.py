from django.db import models
from django.db import models
from django.conf import settings
from uuid import uuid4

def protected_file_upload_path(instance, filename):
    """
    Creates a unique path for protected files to prevent direct access.
    """
    return f'protected/files/{uuid4()}_{filename}'

def protected_image_upload_path(instance, filename):
    """
    Creates a unique path for protected images.
    """
    return f'protected/images/{uuid4()}_{filename}'

class ProtectedFileBase(models.Model):
    """
    An abstract base model for all protected files.
    """
    file = models.FileField(upload_to=protected_file_upload_path)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        
class ProtectedImageBase(models.Model):
    """
    An abstract base model for all protected images.
    """
    image = models.ImageField(upload_to=protected_image_upload_path)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True

"""
from django.http import HttpResponse

def serve_protected_file(request, file_id):
    # This is a simplified example. You'd check permissions here.
    file_object = UserDocument.objects.get(id=file_id)

    if request.user == file_object.owner:
        # Construct the path for Nginx. It's relative to the Nginx root.
        response = HttpResponse()
        response['X-Accel-Redirect'] = '/protected/files/' + file_object.file.name.split('/')[-1]
        return response
    
    return HttpResponse(status=403) # Forbidden
"""
