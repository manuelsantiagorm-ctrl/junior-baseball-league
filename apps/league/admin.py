from django.contrib import admin
from .models import Player, Team

class PlayerInline(admin.TabularInline):
    model = Player
    extra = 0


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'category']
    list_filter = ['category', 'city']
    search_fields = ['name', 'city']
    inlines = [PlayerInline]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'position', 'birth_date', 'team']
    list_filter = ['team', 'position']
    search_fields = ['name', 'team__name']
    list_select_related = ['team']
