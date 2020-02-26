from django.urls import path
from django.views.generic import TemplateView

from festival import views

app_name = 'festival'
urlpatterns = [  
    path('', views.Index.as_view(template_name='index.html'), name='index'),
    path('requests/', views.ManageRequests.as_view(), name='requests'),
    path('request/', views.RequestView.as_view(), name='request'),
    path('request_status/<int:pk>/', views.RequestStatus.as_view(), name='request_status'),
    path('vote/<int:request_id>/', views.VoteView.as_view(), name='voice_create'),
    path('change_status/', views.change_status),
    path('contacts/', TemplateView.as_view(template_name='contacts.html')),
]