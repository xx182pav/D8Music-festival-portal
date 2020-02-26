from django.urls import path, reverse_lazy

from django.contrib.auth.views import LoginView, LogoutView
from users import views

app_name = 'users'
urlpatterns = [  
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(  
        template_name='register.html',  
		success_url=reverse_lazy('users:profile-create')  
    ), name='register'), 
    path('profile-create/', views.CreateUserProfile.as_view(), name='profile-create'),
]