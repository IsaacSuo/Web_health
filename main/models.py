from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TimeSlot(models.Model):
    """十二时辰模型"""
    TIME_CHOICES = [
        ('zi', '子时 (23:00-01:00)'),
        ('chou', '丑时 (01:00-03:00)'),
        ('yin', '寅时 (03:00-05:00)'),
        ('mao', '卯时 (05:00-07:00)'),
        ('chen', '辰时 (07:00-09:00)'),
        ('si', '巳时 (09:00-11:00)'),
        ('wu', '午时 (11:00-13:00)'),
        ('wei', '未时 (13:00-15:00)'),
        ('shen', '申时 (15:00-17:00)'),
        ('you', '酉时 (17:00-19:00)'),
        ('xu', '戌时 (19:00-21:00)'),
        ('hai', '亥时 (21:00-23:00)'),
    ]
    
    name = models.CharField(max_length=10, choices=TIME_CHOICES, unique=True, verbose_name='时辰名称')
    chinese_name = models.CharField(max_length=20, verbose_name='中文名称')
    meridian = models.CharField(max_length=20, verbose_name='对应经络')
    organ = models.CharField(max_length=20, verbose_name='对应脏腑')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    description = models.TextField(verbose_name='经络气血描述')
    health_tips = models.TextField(verbose_name='养生要点')
    case_suggestions = models.TextField(verbose_name='案例与建议')
    food_recommendations = models.TextField(verbose_name='饮食推荐')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '时辰信息'
        verbose_name_plural = '时辰信息'
        ordering = ['start_time']
    
    def __str__(self):
        return f"{self.chinese_name} - {self.meridian}"


class TinnitusLog(models.Model):
    """耳鸣日记模型"""
    SEVERITY_CHOICES = [
        (1, '轻微'),
        (2, '轻度'),
        (3, '中度'),
        (4, '重度'),
        (5, '严重'),
    ]
    
    FREQUENCY_CHOICES = [
        ('continuous', '持续'),
        ('intermittent', '间歇性'),
        ('occasional', '偶发'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    date = models.DateField(default=timezone.now, verbose_name='日期')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='时辰')
    severity = models.IntegerField(choices=SEVERITY_CHOICES, verbose_name='严重程度')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, verbose_name='频率')
    duration_minutes = models.IntegerField(verbose_name='持续时间(分钟)')
    symptoms = models.TextField(blank=True, verbose_name='症状描述')
    triggers = models.TextField(blank=True, verbose_name='诱发因素')
    massage_points = models.TextField(blank=True, verbose_name='按摩穴位')
    massage_effect = models.TextField(blank=True, verbose_name='按摩效果')
    mood = models.CharField(max_length=100, blank=True, verbose_name='情绪状态')
    sleep_quality = models.IntegerField(choices=[(i, f'{i}分') for i in range(1, 11)], null=True, blank=True, verbose_name='睡眠质量(1-10分)')
    notes = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '耳鸣日记'
        verbose_name_plural = '耳鸣日记'
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - 严重程度{self.severity}"


class Reminder(models.Model):
    """时辰提醒模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, verbose_name='时辰')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    custom_message = models.TextField(blank=True, verbose_name='自定义提醒内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '时辰提醒'
        verbose_name_plural = '时辰提醒'
        unique_together = ['user', 'time_slot']
    
    def __str__(self):
        return f"{self.user.username} - {self.time_slot.chinese_name} 提醒"


class AcupointMassage(models.Model):
    """穴位按摩记录模型"""
    BODY_PARTS = [
        ('ear', '耳部'),
        ('head', '头部'),
        ('neck', '颈部'),
        ('shoulder', '肩部'),
        ('hand', '手部'),
        ('foot', '足部'),
    ]
    
    name = models.CharField(max_length=50, verbose_name='穴位名称')
    body_part = models.CharField(max_length=20, choices=BODY_PARTS, verbose_name='身体部位')
    location_description = models.TextField(verbose_name='位置描述')
    massage_method = models.TextField(verbose_name='按摩方法')
    benefits = models.TextField(verbose_name='功效说明')
    related_time_slots = models.ManyToManyField(TimeSlot, blank=True, verbose_name='相关时辰')
    image = models.ImageField(upload_to='acupoints/', blank=True, null=True, verbose_name='穴位图片')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '穴位按摩'
        verbose_name_plural = '穴位按摩'
    
    def __str__(self):
        return f"{self.name} ({self.get_body_part_display()})"


class UserProfile(models.Model):
    """用户扩展信息模型"""
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='性别')
    birth_date = models.DateField(null=True, blank=True, verbose_name='出生日期')
    tinnitus_start_date = models.DateField(null=True, blank=True, verbose_name='耳鸣开始日期')
    constitution_type = models.CharField(max_length=50, blank=True, verbose_name='体质类型')
    medical_history = models.TextField(blank=True, verbose_name='病史')
    current_medications = models.TextField(blank=True, verbose_name='当前用药')
    lifestyle_notes = models.TextField(blank=True, verbose_name='生活习惯备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
    
    def __str__(self):
        return f"{self.user.username} 的资料"
