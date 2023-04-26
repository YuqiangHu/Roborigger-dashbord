from django.db import models
from .validators import validate_file_extension
def upload_path(instance, filname):
    return '/'.join(['CSVFILE', str(instance.title), filname])

class Csvfile(models.Model):
    title = models.CharField(max_length=32, blank=False)
    file = models.FileField(blank=False, null=True, upload_to=upload_path, validators=[validate_file_extension])

class Pdfprogress(models.Model):
    title = models.CharField(max_length=32, blank=False)
    csvfile = models.CharField(max_length=32, blank=False)