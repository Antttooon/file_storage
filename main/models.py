import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename(object):
    def __call__(self, instance, filename):
        return os.path.join(filename[:2], filename)


upload_path = PathAndRename()


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class File(models.Model):
    file = models.FileField(
        upload_to=upload_path,
        storage=OverwriteStorage(),
        unique=True
    )

    def get_absolute_url(self):
        return self.file.url

    def get_filename(self):
        return self.file.name[3:]
