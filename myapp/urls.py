from django.urls import path, include
from .views import register_teacher, register_student, user_login, Logout, AskViewDoubt, ListDoubt
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register_student',register_student, name='register_student'),
    path('register_teacher', register_teacher, name='register_teacher'),
    path('login', obtain_auth_token, name="login"),
    path('user_logout',Logout.as_view(),name='user_logout'),
    path('doubts/',AskViewDoubt.as_view(), name= 'AskViewDoubt'),
    path('teacher_doubts/',ListDoubt.as_view(), name = 'ListDoubt')

]