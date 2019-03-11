from django.contrib import admin
from .models import ReadNum,ReadDetial

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'content_object')

@admin.register(ReadDetial)
class ReadDetial(admin.ModelAdmin):
    list_display = ('date', 'read_num', 'content_object')

