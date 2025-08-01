from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 主页
    path('', views.home, name='home'),
    
    # 时辰相关
    path('time-slot/<str:slot_name>/', views.time_slot_detail, name='time_slot_detail'),
    path('api/current-time-slot/', views.get_current_time_slot, name='current_time_slot_api'),
    
    # 耳鸣养生助手
    path('tinnitus-helper/', views.tinnitus_helper, name='tinnitus_helper'),
    path('tinnitus-log/create/', views.tinnitus_log_create, name='tinnitus_log_create'),
    path('tinnitus-log/list/', views.tinnitus_log_list, name='tinnitus_log_list'),
    
    # 提醒设置
    path('reminder-settings/', views.reminder_settings, name='reminder_settings'),
    
    # 穴位按摩
    path('acupoints/', views.acupoint_list, name='acupoint_list'),
    path('acupoints/<int:acupoint_id>/', views.acupoint_detail, name='acupoint_detail'),
    
    # 用户相关
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    
    # 认证相关
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    
    # 关于我们
    path('about/', views.about, name='about'),
]