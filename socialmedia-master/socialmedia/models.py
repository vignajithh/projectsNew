from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Posts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200,null=True,blank=True)
    post_image=models.ImageField(upload_to="post-images")
    created_date=models.DateTimeField(auto_now_add=True)
    

    def __str__(self) -> str:
        return self.title
    
class UserProfile(models.Model):
    profile_picture=models.ImageField(upload_to="profilpics",null=True,blank=True)
    bio=models.CharField(max_length=600)
    dob=models.DateField()
    phone=models.CharField(max_length=10)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    liked_posts=models.ManyToManyField(Posts,null=True,related_name="liked_post")
    following=models.ManyToManyField(User,related_name="following",null=True)
    followers=models.ManyToManyField(User,related_name="followers",null=True)

    def __str__(self) -> str:
        return self.user.username
    


    


class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.text


class Stories(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    picture=models.ImageField(upload_to="storiesimages")
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    
class Likes(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE,related_name="post")
    liked_date=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")