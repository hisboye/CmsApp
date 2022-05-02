from dataclasses import fields
from django.forms import  ModelForm
from .models import Customer, Order,CustomUser
from django import forms
from django.contrib.auth.hashers import make_password 



class CustomerForm(ModelForm):
    class Meta:
        model=Customer
        fields='__all__'
        exclude=['user','surname']


class FormSetting(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        super(FormSetting,self).__init__(*args, **kwargs)

        for field in self.visible_fields():
            field.field.widget.attrs['class']='form-control'


class Create_Order(ModelForm):
    class Meta:
        model=Order
        fields='__all__'

class CustomUserForm(FormSetting):
    first_name=forms.CharField(max_length=100,label="First Name", widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name=forms.CharField(max_length=100,label="Last Name",widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email'}),required=True)
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}),required=True)
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confim Password'}),required=True)
    widget={
        'password':forms.PasswordInput(),
        'password2':forms.PasswordInput()
    }


    def __init__(self, *args, **kwargs):
        super(CustomUserForm,self).__init__(*args,**kwargs)
        if kwargs.get('instance'):
            instance=kwargs.get('instance').__dict__
            self.fields['password'].required=False
            
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial=instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder']= "Enter your Password"

            else:
                self.fields['first_name'].required=True
                self.fields['last_name'].required=True

    def clean_email(self, *args, **kwargs):
        FormEmail=self.cleaned_data['email'].lower()
        if self.instance.pk is None:            #insert
            if CustomUser.objects.filter(email=FormEmail).exists():
                raise forms.ValidationError('The Given mail is already registered')
        else:
            DbEmail=self.Meta.model.objects.get(id=self.instance.pk).email.lower()
            if DbEmail != FormEmail:
                if CustomUser.objects.filter(email=FormEmail).exists():
                    raise forms.ValidationError("the given email is already Registered")
        return FormEmail


    def clean_password(self):
        
        password=self.cleaned_data.get('password')
        password2=self.data.get('password2')
        print(password)
        print(password2)
        if password is None:
            raise forms.ValidationError('password required')
        if password != password2:        
            raise forms.ValidationError('Password Mismatch')
        if self.instance.pk is None:
            if not password:
                return self.instance.password
        return make_password(password)

       

   
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','email','password']



