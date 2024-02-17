from django.urls import path
from userapp import views

urlpatterns= [

    path("signup/",views.SignUpView.as_view(),name="signup"),
    path("",views.SignInView.as_view(),name="signin"),
    path("signout/",views.SignoutView.as_view(),name="signout"),
    path("profile/add/",views.ProfileCreateView.as_view(),name="profile-add"),
    path("profile/",views.ProfileListView.as_view(),name="profile"),
    path("profile/<int:pk>/change/",views.ProfileUpdateView.as_view(),name="profile-change"),
    path("post-add/",views.PostCreateView.as_view(),name="post-add"),
    path("post/<int:pk>/detail/",views.PostDetailview.as_view(),name="post-detail"),
    path("post/<int:pk>/delete/",views.PostDeleteView.as_view(),name="post-delete"),
    path("user/search/",views.USerSearchView.as_view(),name="user-search"),
    path("user/<int:pk>/",views.UserDetailView.as_view(),name="user-detail"),
    path("post/<int:pk>/like/",views.LikeCreateView.as_view(),name="post-like"),
    path("post/<int:pk>/likes/remove/",views.LikesDeleteView.as_view(),name="likes-remove"),
    path("post/<int:pk>/comment/add/",views.CommentsCreateview.as_view(),name="comment-add"),
    path("user/<int:pk>/follow/",views.FollowView.as_view(),name="follow"),
    path("user/<int:pk>/unfollow/",views.UnFollowView.as_view(),name="unfollow"),
    path("index/",views.IndexView.as_view(),name="index"),
    path("home/",views.HomeView.as_view(),name="home"),
]
