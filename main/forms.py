from django import forms
from django.contrib.auth.models import User
from .models import TinnitusLog, Reminder, UserProfile, TimeSlot


class TinnitusLogForm(forms.ModelForm):
    """耳鸣日记表单"""
    
    class Meta:
        model = TinnitusLog
        fields = [
            'date', 'time_slot', 'severity', 'frequency', 'duration_minutes',
            'symptoms', 'triggers', 'massage_points', 'massage_effect',
            'mood', 'sleep_quality', 'notes'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_slot': forms.Select(attrs={'class': 'form-control'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'symptoms': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'triggers': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'massage_points': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'massage_effect': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'mood': forms.TextInput(attrs={'class': 'form-control'}),
            'sleep_quality': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'date': '日期',
            'time_slot': '时辰',
            'severity': '严重程度',
            'frequency': '频率',
            'duration_minutes': '持续时间（分钟）',
            'symptoms': '症状描述',
            'triggers': '诱发因素',
            'massage_points': '按摩穴位',
            'massage_effect': '按摩效果',
            'mood': '情绪状态',
            'sleep_quality': '睡眠质量',
            'notes': '备注',
        }


class ReminderForm(forms.ModelForm):
    """提醒设置表单"""
    
    class Meta:
        model = Reminder
        fields = ['time_slot', 'is_active', 'custom_message']
        widgets = {
            'time_slot': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'custom_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class UserProfileForm(forms.ModelForm):
    """用户资料表单"""
    
    class Meta:
        model = UserProfile
        fields = [
            'gender', 'birth_date', 'tinnitus_start_date', 'constitution_type',
            'medical_history', 'current_medications', 'lifestyle_notes'
        ]
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tinnitus_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'constitution_type': forms.TextInput(attrs={'class': 'form-control'}),
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'current_medications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'lifestyle_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'gender': '性别',
            'birth_date': '出生日期',
            'tinnitus_start_date': '耳鸣开始日期',
            'constitution_type': '体质类型',
            'medical_history': '病史',
            'current_medications': '当前用药',
            'lifestyle_notes': '生活习惯备注',
        }


class TimeSlotFilterForm(forms.Form):
    """时辰筛选表单"""
    time_slot = forms.ModelChoiceField(
        queryset=TimeSlot.objects.all(),
        required=False,
        empty_label="选择时辰",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )