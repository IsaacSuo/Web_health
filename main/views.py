from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, time
import json

from .models import TimeSlot, TinnitusLog, Reminder, AcupointMassage, UserProfile
from .forms import TinnitusLogForm, ReminderForm, UserProfileForm


def home(request):
    """首页视图"""
    # 获取所有时辰信息，按时间排序
    time_slots = TimeSlot.objects.all().order_by('start_time')
    
    # 获取当前时辰
    current_time = timezone.now().time()
    current_time_slot = None
    
    for slot in time_slots:
        # 处理跨日的时间段（如子时23:00-01:00）
        if slot.start_time > slot.end_time:
            if current_time >= slot.start_time or current_time < slot.end_time:
                current_time_slot = slot
                break
        else:
            if slot.start_time <= current_time < slot.end_time:
                current_time_slot = slot
                break
    
    context = {
        'time_slots': time_slots,
        'current_time_slot': current_time_slot,
    }
    return render(request, 'main/home.html', context)


def time_slot_detail(request, slot_name):
    """时辰详情视图"""
    time_slot = get_object_or_404(TimeSlot, name=slot_name)
    
    # 获取相关穴位
    related_acupoints = AcupointMassage.objects.filter(related_time_slots=time_slot)
    
    context = {
        'time_slot': time_slot,
        'related_acupoints': related_acupoints,
    }
    return render(request, 'main/time_slot_detail.html', context)


def tinnitus_helper(request):
    """耳鸣养生助手首页"""
    if request.user.is_authenticated:
        # 获取用户最近的耳鸣记录
        recent_logs = TinnitusLog.objects.filter(user=request.user).order_by('-date')[:5]
        
        # 获取用户的提醒设置
        reminders = Reminder.objects.filter(user=request.user, is_active=True)
        
        context = {
            'recent_logs': recent_logs,
            'reminders': reminders,
        }
    else:
        context = {}
    
    return render(request, 'main/tinnitus_helper.html', context)


@login_required
def tinnitus_log_create(request):
    """创建耳鸣日记"""
    if request.method == 'POST':
        form = TinnitusLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, '耳鸣日记记录成功！')
            return redirect('tinnitus_helper')
    else:
        form = TinnitusLogForm()
    
    context = {'form': form}
    return render(request, 'main/tinnitus_log_form.html', context)


@login_required
def tinnitus_log_list(request):
    """耳鸣日记列表"""
    logs = TinnitusLog.objects.filter(user=request.user).order_by('-date')
    context = {'logs': logs}
    return render(request, 'main/tinnitus_log_list.html', context)


@login_required
def reminder_settings(request):
    """提醒设置"""
    time_slots = TimeSlot.objects.all()
    user_reminders = {r.time_slot_id: r for r in Reminder.objects.filter(user=request.user)}
    
    if request.method == 'POST':
        for slot in time_slots:
            is_active = request.POST.get(f'reminder_{slot.id}') == 'on'
            custom_message = request.POST.get(f'message_{slot.id}', '')
            
            reminder, created = Reminder.objects.get_or_create(
                user=request.user,
                time_slot=slot,
                defaults={'is_active': is_active, 'custom_message': custom_message}
            )
            
            if not created:
                reminder.is_active = is_active
                reminder.custom_message = custom_message
                reminder.save()
        
        messages.success(request, '提醒设置已更新！')
        return redirect('reminder_settings')
    
    context = {
        'time_slots': time_slots,
        'user_reminders': user_reminders,
    }
    return render(request, 'main/reminder_settings.html', context)


def acupoint_list(request):
    """穴位列表"""
    body_part = request.GET.get('body_part')
    acupoints = AcupointMassage.objects.all()
    
    if body_part:
        acupoints = acupoints.filter(body_part=body_part)
    
    context = {
        'acupoints': acupoints,
        'body_parts': AcupointMassage.BODY_PARTS,
        'selected_body_part': body_part,
    }
    return render(request, 'main/acupoint_list.html', context)


def acupoint_detail(request, acupoint_id):
    """穴位详情"""
    acupoint = get_object_or_404(AcupointMassage, id=acupoint_id)
    context = {'acupoint': acupoint}
    return render(request, 'main/acupoint_detail.html', context)


def about(request):
    """关于我们页面"""
    return render(request, 'main/about.html')


@login_required
def profile(request):
    """用户资料"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '资料更新成功！')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {'form': form, 'profile': profile}
    return render(request, 'main/profile.html', context)


def register(request):
    """用户注册"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'账户 {username} 创建成功！')
            
            # 自动登录
            user = authenticate(username=username, password=form.cleaned_data.get('password1'))
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def get_current_time_slot(request):
    """API：获取当前时辰信息"""
    current_time = timezone.now().time()
    time_slots = TimeSlot.objects.all()
    
    current_slot = None
    for slot in time_slots:
        if slot.start_time > slot.end_time:  # 跨日时间段
            if current_time >= slot.start_time or current_time < slot.end_time:
                current_slot = slot
                break
        else:
            if slot.start_time <= current_time < slot.end_time:
                current_slot = slot
                break
    
    if current_slot:
        data = {
            'name': current_slot.name,
            'chinese_name': current_slot.chinese_name,
            'meridian': current_slot.meridian,
            'organ': current_slot.organ,
            'health_tips': current_slot.health_tips,
        }
    else:
        data = {'error': '未找到当前时辰信息'}
    
    return JsonResponse(data)
