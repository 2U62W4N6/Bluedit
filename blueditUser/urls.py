from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('', views.showAllUser, name='user-list'),
    path('<int:pk>/', views.show_profile, name='user-profile'),
    path('<int:pk>/edit', views.bio_edit, name='edit-profile')
]
