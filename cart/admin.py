from django.contrib import admin
from .models import *

class ItemInline(admin.TabularInline):
	model = Item
	extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ['creation_date','checked_out']
	inlines = [ ItemInline, ]

admin.site.register(Item)
