from django.urls import path 
from . import views

urlpatterns=[
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('upload/', views.upload_resume, name='upload_resume'),
    path('analyze/<int:resume_id>/', views.analyze_resume, name='analyze_resume'),
    path('history/', views.get_history, name='get_history'),
    path('match/<int:resume_id>/', views.match_with_jd, name='match_with_jd'),

]