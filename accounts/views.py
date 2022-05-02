from email import message
from telnetlib import STATUS

from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from accounts.decorators import unauthenticated
from .email_backend import EmailBackend
from .forms import *
from .models import *
from django.conf import settings
from django.db.models.signals import post_save







@unauthenticated
def account_login(request):
    
    if request.method=="POST":
        user=EmailBackend.authenticate(request,username=request.POST.get('email'),password=request.POST.get('password'))
        if user!=None:
            login(request,user)
            if user.user_type == '1':
                return redirect('dashboard')

            if user.user_type =='2':
                return redirect('cms')

        else:
            messages.error(request,'Invalid Login Parameters')
            return redirect('login')
        
    context={}
    return render(request,'login.html',context)

def account_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Thanks for Checking on CMS Goodbye!!")
        return redirect('login')

    else:
        messages.error(request,"You need to Login to be able to accsss this Software")
        return redirect('login')
    


@unauthenticated
def register(request):
    userForm=CustomUserForm(request.POST or None)
    if request.method=='POST':
    
        if userForm.is_valid():
            
            user=userForm.save(commit=False)

            
            user.cms=user
            user.save()
            messages.success(request,'Account Created for' + str(user))
            return redirect('login')

        else:
            messages.error(request,'Invalid Parameters')
   
    context={
        'form':userForm
    }
    return render(request,'register.html',context)

        
    
    
        

