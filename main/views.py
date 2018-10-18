from django.shortcuts import render, HttpResponse, redirect
from django.http import FileResponse
from django.contrib import messages
from django.urls import reverse
from .forms import UploadFileForm
from .models import File
from django.conf import settings
# Create your views here.
from django.db.utils import IntegrityError

import os
import mimetypes
import hashlib

def main(request):
    print('MAIN view - OK')
    file = None
    files = File.objects.all()[::-1]
    if request.is_ajax():
        print("REQUEST POST")
        # if request.is_ajax():
        print("REQUEST IS AJAX")
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("FORM VALID")
            instance = form.save()
            file = instance.file.name[3:]
            data = file
            return HttpResponse(data)

    form = UploadFileForm()

    return render(request, 'main.html', {'form':form,
                                         'file':file,
                                         'files':files})

def file_upload(request):
    if request.method == 'POST':
        if request.is_ajax():
            print("THIS AJAX")
            form = UploadFileForm(request.POST, request.FILES or None)
            # print("files", request.FILES)
            if form.is_valid():
                print("FORM VALID")
                try:
                    instance = form.save()
                except IntegrityError:
                    return HttpResponse("File dublicate error: This file has already been uploaded")
                res = "<p> File uploaded:  {}</p>".format(instance.file.name[3:])
                # data = file
                return HttpResponse(res)
            return HttpResponse("No" + str(request.FILES) + str(request.POST))
        else:
            print("NO AJAX")
            if request.method == "POST":
                print(request.FILES)

            return HttpResponse('Nonono')

def search(search_string):
    print("START SEARCH ------------------------!")
    search_request = search_string[:2]+'/'+search_string
    try:
        res = File.objects.filter(file=search_request).first()
    except:
        res = None

    return res

def get_file_path(object):
    print(object)
    if isinstance(object, File):
        path = settings.BASE_DIR + object.get_absolute_url()
        print('PATH', path)
        return str(path)


def download(request):
    if request.method == "POST":
        search_string = request.POST['filename']
        if search_string is not None:
            res = search(search_string)
            file_path = get_file_path(res)
            print("FILE PATH IN DOWNLOAD", file_path)
            if file_path:
                try:
                    resp = FileResponse(open(file_path, 'rb'))
                except FileNotFoundError:
                    return HttpResponse('FileNotFoundError')

                resp['Content-Type'] = mimetypes.guess_type(search_string)[0]
                resp['Content-Disposition'] = 'attachment; filename=%s' % search_string
                return resp

            return HttpResponse('FileNotFoundError')
    return redirect('/')

def delete(request):
    print("START DELETE --------------------")
    if request.method == "GET" and request.is_ajax():
        search_string = request.GET['filename']
        print("SEARCH STRING", search_string)
        if search_string is not None:

            res = search(search_string)
            if res:
                db_row = File.objects.filter(file=res.file)
                if db_row:
                    db_row.delete()
            file_path = get_file_path(res)
            print("FILE_PATH", file_path)
            print("RES + = ", res)
            # print("FILE PATH in DELETE VIEW = ",file_path)
            if file_path:
                try:
                    os.remove(file_path)
                except FileNotFoundError:
                    return HttpResponse('FileNotFoundError')

                if not os.path.exists(file_path):
                    return HttpResponse('File deleted - {}'.format(search_string))
            return HttpResponse('FileNotFoundError')
    return redirect('/')

