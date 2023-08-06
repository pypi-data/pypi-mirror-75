from django.contrib import admin

from . import models


@admin.register(models.Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'party', 'is_active', 'create_time')
    raw_id_fields = ('party', 'user')
    search_fields = ("title",)
    readonly_fields = ('party',)
    date_hierarchy = 'create_time'


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('create_time', '__str__')
    raw_id_fields = ('party', 'user', 'paper')
    search_fields = ("paper__title",)
    # readonly_fields = ('party',)


@admin.register(models.Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('paper',)
    raw_id_fields = ('party', 'paper')


@admin.register(models.Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('paper', 'user', 'create_time')
    list_select_related = ['paper', 'user']
    raw_id_fields = ('party', 'user', 'paper')
    search_fields = ("paper__title", "user__first_name")
    # readonly_fields = ('party',)


@admin.register(models.Fault)
class FaultAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'user_id', 'paper_id', 'question_id', 'times', 'corrected', 'update_time')
    list_filter = ('corrected',)
    date_hierarchy = 'update_time'
    raw_id_fields = ('party', 'paper', 'user')
    readonly_fields = ('update_time', 'create_time')


@admin.register(models.Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'name', 'target_user_tags', 'target_user_count', 'is_active', 'begin_time','minutes', 'end_time')
    list_filter = ('is_active',)
    date_hierarchy = 'begin_time'
    raw_id_fields = ('party', 'target_users')
    readonly_fields = ('target_users', 'create_time')
