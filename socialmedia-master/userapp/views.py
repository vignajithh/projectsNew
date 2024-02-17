from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import View,FormView,DetailView,UpdateView,ListView,CreateView,TemplateView
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from userapp.forms import SignUpForm,SignInForm,UserProfileForm,PostForm,UserSearchForm,CommentForm
from socialmedia.models import UserProfile,Posts,Likes,Comments
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

# Create your views here.

def SigninRequired(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

            

class SignUpView(CreateView):
    template_name="signup.html"
    form_class=SignUpForm
    success_url=reverse_lazy("signin")
    
        
class SignInView(FormView):
    form_class=SignInForm
    template_name="signin.html"

    def post(self,request,*args,**kwargs):
        form=SignInForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_obj=authenticate(request,username=u_name,password=pwd)
            if user_obj:
                login(request,user_obj)
                print("session started")
                return redirect("home")
            else:
                print("login failed")
                return render(request,"signin.html",{"form":form})
        print("form invalid")
        return render(request,"signin.html",{"form":form})
    
class SignoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        print("session ended")
        return redirect("signin")

@method_decorator(SigninRequired,name="dispatch")    
class ProfileCreateView(CreateView):
    template_name="user-profile.html"
    form_class=UserProfileForm
    model=UserProfile
    success_url=reverse_lazy("profile")

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

    
@method_decorator(SigninRequired,name="dispatch")        
class ProfileListView(View): # post list also
    def get(self,request,*args,**kwargs):
        qs=UserProfile.objects.filter(user=request.user)
        ps=Posts.objects.filter(user=request.user)
        fs=request.user.profile.following.all()
        frs=request.user.profile.followers.all()
        return render(request,"profile-list.html",{"data":qs,"post":ps,"following":fs,"followers":frs})

@method_decorator(SigninRequired,name="dispatch")        
class ProfileUpdateView(UpdateView):
    form_class=UserProfileForm
    template_name="profile-edit.html"
    model=UserProfile
    success_url=reverse_lazy("profile")


@method_decorator(SigninRequired,name="dispatch")        
class PostCreateView(CreateView):
    template_name="posts-add.html"
    form_class=PostForm
    model=Posts
    success_url=reverse_lazy("profile")

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)


    
@method_decorator(SigninRequired,name="dispatch")       
class PostDetailview(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Posts.objects.get(id=id)
        ls=Likes.objects.filter(post=id).order_by("-liked_date")
        return render(request,"post_detail.html",{"data":qs,"likes":ls})

@method_decorator(SigninRequired,name="dispatch")    
class PostDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Posts.objects.get(id=id).delete()
        return redirect("profile")
    

@method_decorator(SigninRequired,name="dispatch")    
class USerSearchView(FormView):
    template_name="user-search.html"
    form_class=UserSearchForm

    def post(self,request,*args,**kwargs):
        form=UserSearchForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            qs=User.objects.filter(username__icontains=u_name)
            return render(request,"user-search.html",{"data":qs})

@method_decorator(SigninRequired,name="dispatch")            
class UserDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=UserProfile.objects.filter(user=id)
        ps=Posts.objects.filter(user=id)
        user_object=UserProfile.objects.get(user=id)
        fs=user_object.following.all()
        frs=user_object.followers.all()
        return render(request,"user-list.html",{"data":qs,"post":ps,"following":fs,"followers":frs})

@method_decorator(SigninRequired,name="dispatch")        
class LikeCreateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post_object=Posts.objects.get(id=id)
        Likes.objects.create(post=post_object,user=request.user)
        request.user.profile.liked_posts.add(post_object)
        return redirect("post-detail",pk=id)
    

@method_decorator(SigninRequired,name="dispatch")    
class LikesDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post_object=Posts.objects.get(id=id)
        Likes.objects.get(post=id,user=request.user).delete()
        request.user.profile.liked_posts.remove(post_object)
        
        return redirect("post-detail",pk=id) 

@method_decorator(SigninRequired,name="dispatch")    
class CommentsCreateview(View):
    def get(self,request,*args,**kwargs):
        form=CommentForm()
        id=kwargs.get("pk")
        com=Comments.objects.filter(post=id).order_by("-created_date")
        return render(request,"comments.html",{"form":form,"comments":com})
    
    def post(self,request,*args,**kwargs):
        form=CommentForm(request.POST)
        if form.is_valid():
            form.instance.user=self.request.user
            form.instance.post=get_object_or_404(Posts,pk=kwargs.get("pk"))
            form.save()
            return redirect("comment-add",pk=kwargs.get("pk"))
        return render(request,"comments.html",{"form":form})
    
@method_decorator(SigninRequired,name="dispatch")    
class FollowView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        follow_object=UserProfile.objects.get(id=id)
        request.user.profile.following.add(follow_object.user)
        follow_object.followers.add(request.user)
        return redirect("user-detail",pk=id)

@method_decorator(SigninRequired,name="dispatch")            
class UnFollowView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        follow_object=UserProfile.objects.get(id=id)
        request.user.profile.following.remove(follow_object.user)
        follow_object.followers.remove(request.user)
        return redirect("user-detail",pk=id)
     
@method_decorator(SigninRequired,name="dispatch")        
class IndexView(View):
    def get(self,request,*args,**kwargs):
        followings=request.user.profile.following.all()
        qs=Posts.objects.filter(user__in=followings).order_by("-created_date")
        return render(request,"index.html",{"post":qs})

@method_decorator(SigninRequired,name="dispatch")    
class HomeView(TemplateView):
    template_name="home.html"
    


      
        