from django.contrib import admin
from .models import *
import datetime

class ItemInline(admin.TabularInline):
	model = Item
	extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ['creation_date','checked_out']
	inlines = [ ItemInline, ]
	def delete_queryset(self, request, queryset):
		today = datetime.datetime.today()
		for obj in queryset:
			t = False
			if (today.year == obj.creation_date.year and obj.creation_date.month == today.month and obj.creation_date.day == today.day):
				t = True
			if not obj.checked_out and not t:
				obj.delete()

admin.site.register(Item)
