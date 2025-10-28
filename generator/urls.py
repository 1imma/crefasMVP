from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_toolkit_view, name='ai_toolkit'),
]
