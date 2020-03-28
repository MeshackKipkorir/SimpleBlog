from django.shortcuts import render,redirect
from .forms import AddBlogForm,UserForm,UserProfileInfoForm
from .models import Post
import datetime,timeago,timedelta
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
# Create your views here.


def index(request):

    content = Post.objects.all().filter(status='published').order_by('-created')
    context = {'content':content}
    return render(request,'index.html',context)

@login_required
def add_blog(request):
    form = AddBlogForm()
    
    if request.method == "POST":
        form = AddBlogForm(request.POST)
        if form.is_valid():
            form.save()
            form = AddBlogForm()
            return redirect('index')
    context = {'form':AddBlogForm}
    return render(request,'add_blog.html',context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profileForm = UserProfileInfoForm(data = request.POST)

        if user_form.is_valid and profileForm.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profileForm.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES['profile_pic']:
                print('profile pic present')
                profile.profile_pic = request.FILES['profile_pic']

            profile.Save()
            registered = True
        
        else:
            print(UserForm.errors,profileForm.errors)

    else:
        user_form = UserForm()
        profileForm = UserProfileInfoForm()

    context = {
        'user_form':UserForm,
        'profileForm':UserProfileInfoForm,
        'registered':registered
    }
    return render(request,'registration.html',context)

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active():
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponseRedirect('please reactivate your account')
        else:
            return HttpResponse('Invalid login details given')
    else:
        return render(request,'login.html')
        
