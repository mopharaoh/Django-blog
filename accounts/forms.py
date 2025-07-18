from django import forms
from django.contrib.auth.forms import AuthenticationForm , PasswordResetForm , SetPasswordForm ,PasswordChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class PwdChangeForm(PasswordChangeForm):
    old_password=forms.CharField(label='Old password',widget=forms.PasswordInput(
        attrs={'class':'form-control mb-3',
               'placeholder':'Old Password','id':'form-oldpass'}))
    
    new_password1=forms.CharField(label='New password',widget=forms.PasswordInput(
        attrs={'class':'form-control mb-3',
               'placeholder':'New Password','id':'form-newpass'}))
    
    new_password2=forms.CharField(label='Repeat password',widget=forms.PasswordInput(
        attrs={'class':'form-control mb-3',
               'placeholder':'New Password','id':'form-new-pass2'}))

class UserEditForm(forms.ModelForm):
    first_name=forms.CharField(label="Firstname",max_length=30,widget=forms.TextInput(
        attrs={'class':'form-control mb-3','placeholder':'First Name','id':'form-firstname'}))
    last_name=forms.CharField(label="Lastname",max_length=30,widget=forms.TextInput(
        attrs={'class':'form-control mb-3','placeholder':'Last Name','id':'form-lastname'}))
    email=forms.EmailField(max_length=254,widget=forms.EmailInput(
        attrs={'class':'form-control mb-3','placeholder':'Email','id':'form-email'}))
    
    class Meta:
        model=User
        fields=('first_name','last_name','email')
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('please use another one, this email is already taken')
        return email
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        


class PwdResetConfirmForm(SetPasswordForm):
    new_password1=forms.CharField(
        label='New password',widget=forms.PasswordInput(
            attrs={'class':'form-control mb-3',
               'placeholder':'New Password','id':'form-newpass'}))
    
    new_password2=forms.CharField(
        label='Repeat password',widget=forms.PasswordInput(
            attrs={'class':'form-control mb-3',
               'placeholder':'New Password','id':'form-new-pass2'}))
    

class PwdResetForm(PasswordResetForm):

    email=forms.EmailField(max_length=254,widget=forms.TextInput(
        attrs={'class':'form-control mb-3',
               'placeholder':'Email','id':'form-email'}))
    def clean_email(self):
        email=self.cleaned_data['email']
        test=User.objects.filter(email=email)
        if not test:
            raise ValidationError('can not find that email')
        return email
    


class UserLoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control mb-3','placeholder':'Username','id':'login-username'}
    ))
    password=forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder':'Password','id':'login-pwd'}
    ))


class RegistrationForm(forms.ModelForm):

    username=forms.CharField(
        label='Enter Username',min_length=4,max_length=50,help_text='Required'
    )
    email= forms.EmailField(max_length=100,help_text='Required',error_messages={'required':'sorry you will need an email'})
    password=forms.CharField(label='Password',widget=forms.PasswordInput)
    password2=forms.CharField(label='Repeat password',widget=forms.PasswordInput)
    
    class Meta:
        model=User
        fields=('username','email','first_name')

    def clean_username(self):
        username=self.cleaned_data['username'].lower()
        r=User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Passwords do not match.')
        return cd['password2']
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('please use another one')
        return email
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs.update(
            {'class':'form-control mb-3','placeholder':'Username'}
        )
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})