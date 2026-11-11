from django.contrib import admin
from .models import Category, Profession, Group, News, Application, Photo, Review, FAQ


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


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'profession', 'status', 'created_at')
    list_filter = ('status', 'profession')
    search_fields = ('name', 'phone')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'published')
    list_editable = ('order', 'published')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'profession', 'rating', 'published')
    list_filter = ('published', 'rating')
    list_editable = ('published',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'published')
    list_editable = ('order', 'published')