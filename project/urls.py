"""Hub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from project.views import *

urlpatterns = [
    path('', ProjectListView.as_view()),
    path('pm/', ProjectListByPMView.as_view()),
    path('status/', ProjectListByStatusView.as_view()),
    path('<int:pk>/', ProjectRetrieveView.as_view()),
    path('create/', ProjectCreateView.as_view()),
    path('update_destroy/<int:pk>/', ProjectUpdateDestroyView.as_view()),
]
