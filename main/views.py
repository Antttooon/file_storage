from django.shortcuts import render, HttpResponse, redirect
from django.http import FileResponse
from .forms import UploadFileForm
from .models import File
from django.conf import settings
from django.db.utils import IntegrityError

import os
import mimetypes

def main(request):
    file = None
    files = File.objects.all()[::-1]
    if request.is_ajax():
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            file = instance.file.name[3:]
            return HttpResponse(file)

    form = UploadFileForm()
    return render(request, 'main.html', {'form': form,
                                         'file': file,
                                         'files': files})


def file_upload(request):
    if request.method == 'POST':
        if request.is_ajax():
            form = UploadFileForm(request.POST, request.FILES or None)
            if form.is_valid():
                try:
                    instance = form.save()
                except IntegrityError:
                    return HttpResponse("File dublicate error: This file has already been uploaded")
                res = "<p> File uploaded:  {}</p>".format(instance.file.name[3:])
                return HttpResponse(res)
            return HttpResponse("No" + str(request.FILES) + str(request.POST))
        else:
            return HttpResponse('Nonono')


def search(search_string):
    search_request = search_string[:2] + '/' + search_string
    try:
        res = File.objects.filter(file=search_request).first()
    except:
        res = None
    return res


def get_file_paths(object):
    if isinstance(object, File):
        path_file = os.path.join(settings.BASE_DIR, object.get_absolute_url()[1:])
        folder = object.get_absolute_url().split('/')
        path_folder = os.path.join(settings.BASE_DIR, folder[1], folder[2])
        return path_file, path_folder


def download(request):
    if request.method == "POST":
        search_string = request.POST['filename']
        if search_string is not None:
            res = search(search_string)
            file_paths = get_file_paths(res)
            if file_paths:
                try:
                    resp = FileResponse(open(file_paths[0], 'rb'))
                except FileNotFoundError:
                    return HttpResponse('File Not Found')

                resp['Content-Type'] = mimetypes.guess_type(search_string)[0]
                resp['Content-Disposition'] = 'attachment; filename=%s' % search_string
                return resp

            return HttpResponse('File Not Found')
    return redirect('/')


def delete(request):
    if request.method == "GET" and request.is_ajax():
        search_string = request.GET['filename']
        if search_string is not None:
            res = search(search_string)
            if res:
                db_row = File.objects.filter(file=res.file)
                if db_row:
                    db_row.delete()
            file_paths = get_file_paths(res)
            if file_paths:
                try:
                    os.remove(file_paths[0])
                    os.rmdir(file_paths[1])
                except FileNotFoundError:
                    return HttpResponse('File Not Found')

                if not os.path.exists(file_paths[0]):
                    return HttpResponse('File deleted - {}'.format(search_string))
            return HttpResponse('File Not Found')
    return redirect('/')
