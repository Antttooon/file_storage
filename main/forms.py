from django import forms
from .models import File

from file_storage.settings import MEDIA_ROOT
import os
import hashlib

# class UploadFileForm(forms.Form):
#     file = forms.FileField()
#
#     # class Meta:
#     #     model = File
#     #     fields = ['file',]
#
#     def handle_uploaded_file(self, f, file_name):
#         # print('NAME = ', type(str(f)))
#         file_path = MEDIA_ROOT+'/'+ str(file_name)[:2]+'/'+str(file_name)
#         # file_path = os.path.join()
#         print('FILE PATH = ',file_path)
#         print("PATH = ", os.getcwd())
#         with open(file_path, 'wb+') as destination:
#             for chunk in f.chunks():
#                 destination.write(chunk)
#
#     def save(self):
#         print("Form SAVE", self.cleaned_data)
#         file_hash = self.cleaned_data['file']
#         # print("2", dir(file_hash))
#         print("FILE = ", file_hash)
#         file_object = file_hash.read()
#         self.file = hashlib.sha256(file_object).hexdigest()
#         print('SELF FILE = ', self.file)
#         # super(UploadFileForm, self).save()
#         # File.objects.create(file=self.file)
#         # self.handle_uploaded_file(file_hash, self.file)


class UploadFileForm(forms.ModelForm):
    file = forms.FileField()
    class Meta:
        model = File
        exclude = ()

    def save(self):
        self.instance = super(UploadFileForm, self).save(commit=False)
        file_object = self.cleaned_data['file'].read()
        self.instance.file.name = hashlib.sha256(file_object).hexdigest()
        self.instance.save()
        return self.instance


# 08783aa63e3a43df5b7d5bde502968d3d4db51bc79ba43fbd6148c6ad9021f32
# 1917be5d763e664516ed6b62114f245fc2c499e11ea6a9012f8dc3d9bffbeddd