from django.contrib import admin

# Register your models here.
from .models import Todo


@admin.register(Todo)
class Todoadmin(admin.ModelAdmin):
    list_display=['title','completed','created_at']
    list_filter=['completed','created_at']
    search_fields=['title']