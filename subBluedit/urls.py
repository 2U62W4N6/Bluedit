from django.urls import path
from . import views

urlpatterns = [
    path('', views.AllSubs, name='sub-list'),
    path('newSub/', views.CreateSub,name='sub-create'),

    path('<int:pk>/', views.OneSub, name='sub'),
    path('<int:pk>/follow', views.Follow, name='follow'),
    path('<int:pk>/unfollow', views.UnFollow, name='unfollow'),
    # Edit Subscriber-Levels
    path('<int:pk>/editAbo', views.setRole_or_Ban, name='editAbo'),
    
    path('<int:pk_sub>/posts/<int:pk_post>', views.PostDetail, name='post'),
    path('post/vote/<int:pk>/<int:up_or_down>', views.VotePost, name='post-vote'),
    path('<int:pk_sub>/posts/<int:pk_post>/edit', views.PostEdit, name='post-edit'),
    path('<int:pk>/posts/newpost/text', views.CreateTextPost, name='post-create-text'),
    path('<int:pk>/posts/newpost/media', views.CreateMediaPost, name='post-create-media'),
    
    path('comment/vote/<int:pk>/<int:up_or_down>', views.VoteComment, name='comment-vote'),
    path('<int:pk_sub>/posts/<int:pk_post>/<int:pk_comment>', views.CommentDetail, name='comment'),
    path('<int:pk_sub>/posts/<int:pk_post>/<int:pk_comment>/edit', views.CommentEdit, name='editcomment'),
]
