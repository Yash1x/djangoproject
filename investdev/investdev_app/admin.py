from django.contrib import admin
from .models import Publication, Category, InvestmentFactor, ProjectPassport


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'is_published', 'category', 'passport')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_published', 'category')
    filter_horizontal = ('factors',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(InvestmentFactor)
class InvestmentFactorAdmin(admin.ModelAdmin):
    list_display = ('id', 'factor', 'slug')
    list_display_links = ('id', 'factor')
    search_fields = ('factor',)
    prepopulated_fields = {'slug': ('factor',)}


@admin.register(ProjectPassport)
class ProjectPassportAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_code', 'initiator', 'budget_mln_rub', 'horizon_years')
    list_display_links = ('id', 'project_code')
    search_fields = ('project_code', 'initiator')
