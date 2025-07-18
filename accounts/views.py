from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str , force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm,UserEditForm
from .token import account_activation_token
from django.contrib.auth.models import User


@login_required
def profile(request):
    return render(request,'accounts/profile.html',{'section':'profile'})


def accounts_register(request):
    if request.method == 'POST':
        registerForm=RegistrationForm(request.POST)
        if registerForm.is_valid():
            user=registerForm.save(commit=False)
            user.email=registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active=False
            user.save()
            current_site=get_current_site(request)
            subject='Activate your Account'
            message=render_to_string('registration/account_activation_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            user.email_user(subject=subject,message=message)
            return HttpResponse('registered succesfully and activation sent')

    else:
        registerForm=RegistrationForm()
    return render(request,'registration/register.html',{'form':registerForm})


def activate(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)

    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        login(request,user) ###
        return redirect('login')
    else:
        return render(request,'registration/activation_invalid.html')
    
@login_required
def edit(request):
    if request.method == 'POST':
        user_form=UserEditForm(request.POST,instance=request.user)
        if user_form.is_valid():
            user_form.save()
            
    else:
        user_form=UserEditForm(instance=request.user)
    return render(request,'accounts/update.html',{'user_form':user_form})
@login_required
def delete_user(request):
    if request.method == 'POST':
        user=User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        return redirect('accounts:login')
    return render(request,'accounts/delete_user.html')