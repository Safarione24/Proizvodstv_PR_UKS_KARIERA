from django.contrib import admin
from .models import Category, Profession, Group, News


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'published')
    list_filter = ('category', 'published')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('profession', 'category', 'start_date', 'exam_date', 'published')
    list_filter = ('category', 'published', 'start_date')
    search_fields = ('profession__name',)
    date_hierarchy = 'start_date'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'published')
    list_filter = ('published',)
    search_fields = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)}