from django.urls import path
from . import views


app_name = 'conversacion'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:pk>/', views.detail, name='detail'),
    path('new/<slug:slug>/', views.new_conversation, name='new'),
    
]