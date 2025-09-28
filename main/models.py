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

