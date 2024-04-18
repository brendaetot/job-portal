"""
URL configuration for jobportal_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('regapplicant', views.regapplicant, name='regapplicant'),
    path('signup', views.signup, name='signup'),
    path('base', views.base, name='base'),
    path('regemployer/', views.regemployer, name='regemployer'),
    path('addjobs', views.addjobs, name='addjobs'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('login_recruiter', views.login_recruiter, name='login_recruiter'),
    path('login_applicant', views.login_applicant, name='login_applicant'),
    path('applicant_dashboard/', views.applicant_dashboard, name='applicant_dashboard'),
    path('recruiter_dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('edit_job/<id>/', views.edit_job, name='edit_job'),
    
    path('delete_job/<job_id>/', views.delete_job, name='delete_job'),

]
