from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from socialmedia.models import UserProfile,Posts,Comments


class SignUpForm(UserCreationForm):
    password1=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={"class":"form-control"}))

    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password1","password2"]
        widgets={
            "first_name": forms.TextInput(attrs={"class":"form-control"}),
            "last_name": forms.TextInput(attrs={"class":"form-control"}),
            "username": forms.TextInput(attrs={"class":"form-control"}),
            "email": forms.EmailInput(attrs={"class":"form-control"}),
        }

class SignInForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=["profile_picture","bio","dob","phone"]
        widgets={
            "profile_picture":forms.FileInput(attrs={"class":"form-control"}),
            "dob":forms.DateInput(attrs={"type":"date","class":"form-control"}),
            "bio":forms.TextInput(attrs={"class":"form-control"}),
            "phone":forms.TextInput(attrs={"class":"form-control"}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=["title","post_image"]
        widgets={
            "post_image":forms.FileInput(attrs={"class":"form-control"})
        }

class UserSearchForm(forms.Form):
    username=forms.CharField()

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=["text"]