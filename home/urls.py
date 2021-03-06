"""PostgreSLQ_DEMO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from .views import index, delete_human, update_human, basic_df_setup, basic_setup, create_home_gender, create_home_human
from django.urls import path


urlpatterns = [
    path('', index),
    path('basic_setup', basic_setup),
    path('basic_df_setup', basic_df_setup),
    path('create_home_gender', create_home_gender),
    path('create_home_human', create_home_human),
    path('delete/<int:human_id>', delete_human),
    path('update/<int:human_id>', update_human),
]
