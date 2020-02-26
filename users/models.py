from django.db import models

from django.contrib.auth.models import User  
  
  
class UserProfile(models.Model):    
    info = models.TextField('Информация о заявителе', blank=True, null=True)  
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return self.user.username

