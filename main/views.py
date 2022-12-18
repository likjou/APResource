from http.client import HTTPResponse
from unicodedata import category
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .models import TorFile
from .forms import UploadFile, UpdateUserForm
from django.contrib.auth.decorators import login_required
from torrentool.api import Torrent
from django.conf import settings

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView

# Create your views here.

# def login(response):
#     return render(response, 'register/login.html')

@login_required(login_url="/account/login")
def resources(request):
    all_files = TorFile.objects.all().exclude(user=2)
    return render(request, "main/resources.html",{'all_files':all_files})

@login_required(login_url="/account/login")
def userfile(request,username):
    all_files = TorFile.objects.filter(user__username__icontains=username)
    return render(request, "main/userfile.html",{'all_files':all_files, "username":username})

@login_required(login_url="/account/login")
def filter(request,category):
    all_files = TorFile.objects.all().exclude(user=2)
    cate_files = all_files.filter(category=category)
    return render(request, "main/resources.html",{'all_files':cate_files})
    
@login_required(login_url="/account/login")
def apfilter(request,category):
    all_files = TorFile.objects.filter(user=2)
    cate_files = all_files.filter(category=category)
    return render(request, "main/apfiles.html",{'all_files':cate_files})
    
@login_required(login_url="/account/login")
def myfilter(request,category):
    curr_user = request.user
    all_files = TorFile.objects.filter(user=curr_user.id)
    cate_files = all_files.filter(category=category)
    return render(request, "main/myFiles.html",{'all_files':cate_files,"curr_user":curr_user})

@login_required(login_url="/account/login")
def search(request):
    if request.method == 'POST': #if button pressed

        if request.POST['searched']:    #if search not empty
            searched = request.POST['searched']

            if request.POST['filtered'].lower() == "all category":  #if filter = all category
                all_files = TorFile.objects.filter(title__contains=searched)
                return render(request, "main/search.html",{"all_files":all_files,"searched":searched})
            else:   #if filter not empty
                filtered = request.POST['filtered']
                all_files = TorFile.objects.filter(title__contains=searched)
                filtered = all_files.filter(category__contains=filtered)
                return render(request,"main/search.html", {"all_files":filtered, "searched":searched})

        else:   #if search empty

            if request.POST['filtered'].lower() == "all category":  #if filter = all category
                return redirect("/resources")
            else:   #if filter not empty
                filtered = request.POST['filtered']
                all_files = TorFile.objects.filter(category__contains=filtered)
                return render(request,"main/search.html",{"all_files":all_files})

@login_required(login_url="/account/login")
def fileinfopage(request, id):
    files = TorFile.objects.filter(id=id)
    for file in files:
        filename = str(file.file_field)
        before_upload = settings.MEDIA_ROOT +"/" +str(filename)
        my_torrent = Torrent.from_file(before_upload)
        torrent_name = my_torrent.name
        filelist = my_torrent.files
        
    return render(request, "main/fileinfo.html", {"files":files, "filelist":filelist,"torrent_name":torrent_name})

@login_required(login_url="/account/login")
def myFiles(response):
    curr_user = response.user
    all_files = TorFile.objects.filter(user=curr_user.id) 
    
    return render(response, "main/myFiles.html",{"curr_user":curr_user,"all_files":all_files})

@login_required(login_url="/account/login")
def apfiles(response):
    all_files = TorFile.objects.filter(user=2)
    return render(response, "main/apfiles.html",{
        "all_files":all_files
    })



@login_required(login_url="/account/login")  
def upload(request):
    form = UploadFile()
    context = {'form':form}
    if request.method == 'POST':
        form = UploadFile(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            before_upload = settings.MEDIA_ROOT+ "/" + str(instance.file_field)
            my_torrent = Torrent.from_file(before_upload)
            instance.file_size = convert_bytes(my_torrent.total_size)
            instance.infohash = str(my_torrent.info_hash)
            instance.magnet = str(my_torrent.magnet_link)
            instance.save()
            return redirect('/myFiles')
        else:
            # print(form.errors)
            return render(request, 'main/upload.html',{'form':form})
    return render(request,'main/upload.html', context)

@login_required(login_url="/account/login")
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        
        if user_form.is_valid():
            user_form.save()
            return redirect('/profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
    
    return render(request, 'main/profile.html', {'user_form': user_form})

class ChangePasswordView(PasswordChangeView):
    template_name = 'main/changepass.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('profile')


def convert_bytes(bytes_number):
    tags = [ "Byte", "KB", "MB", "GB", "TB" ]
 
    i = 0
    double_bytes = bytes_number
 
    while (i < len(tags) and  bytes_number >= 1024):
            double_bytes = bytes_number / 1024.0
            i = i + 1
            bytes_number = bytes_number / 1024
 
    return str(round(double_bytes, 2)) + " " + tags[i]
