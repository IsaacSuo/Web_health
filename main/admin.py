from django.contrib import admin
from .models import TimeSlot, TinnitusLog, Reminder, AcupointMassage, UserProfile


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['chinese_name', 'name', 'meridian', 'organ', 'start_time', 'end_time']
    list_filter = ['organ', 'meridian']
    search_fields = ['chinese_name', 'meridian', 'organ']
    ordering = ['start_time']


@admin.register(TinnitusLog)
class TinnitusLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'time_slot', 'severity', 'frequency', 'duration_minutes']
    list_filter = ['severity', 'frequency', 'time_slot', 'date']
    search_fields = ['user__username', 'symptoms', 'triggers']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['user', 'time_slot', 'is_active', 'created_at']
    list_filter = ['is_active', 'time_slot']
    search_fields = ['user__username', 'time_slot__chinese_name']


@admin.register(AcupointMassage)
class AcupointMassageAdmin(admin.ModelAdmin):
    list_display = ['name', 'body_part', 'created_at']
    list_filter = ['body_part']
    search_fields = ['name', 'location_description']
    filter_horizontal = ['related_time_slots']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'birth_date', 'tinnitus_start_date']
    list_filter = ['gender', 'constitution_type']
    search_fields = ['user__username', 'user__email']
