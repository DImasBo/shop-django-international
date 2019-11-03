from django.contrib import admin
from parler.admin import TranslatableAdmin, TranslatableTabularInline 
from django_summernote.admin import SummernoteModelAdmin

from .models import Category, Product, ProductImage 
from .models import Page, Question, Order

@admin.register(Category)
class CategoryeAdmin(TranslatableAdmin):
	list_display = ('name', 'slug')

class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 1

@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin,TranslatableAdmin, admin.ModelAdmin):
	list_display = ('id','title', 'language_column','price','is_publish','status','count','category')	
	list_filter = ('category','status','is_publish')
	inlines = [ ProductImageInline, ]
	summernote_fields = 'description'

	fieldsets = (
		("Інтернаціональні поля", {
			'fields': ('title','description'),
		}),

		("Параметри", {
			'fields': (
				'slug',
				'category',
				'status',
				('price','count','is_publish')
				),
		}),
		("Для пошуку", {
			"fields":("meta_description","meta_keywords")
			}),
		("Медіа контент",{
			"fields":('product_cover',)
			})
	)

@admin.register(Page)
class PageAdmin(SummernoteModelAdmin,TranslatableAdmin):
	list_display = ('title','language_column','is_publish','is_menu')
	list_filter = ('is_publish','is_menu')
	summernote_fields = 'description'

	fieldsets = (
		("Інтернаціональні поля", {
			'fields': ('title','description'),
		}),
		("Параметри", {
			'fields': (
				'slug',
				'is_menu',
				'is_publish',
				),
		}),
		("Для пошуку", {
			"fields":("meta_description","meta_keywords")
			}),
	)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ['name','email','date']

def make_paid(modeladmin, request, queryset):
	queryset.update(status='PAID_status')
def make_ip(modeladmin, request, queryset):
	queryset.update(status='IP_status')
def make_aip(modeladmin, request, queryset):
	queryset.update(status='AIP_status')

make_aip.short_description = 'Помітити як Прийнятий в обробку'
make_ip.short_description = 'Помітити як В обробці'
make_paid.short_description = 'Помітити як Оплачено'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['view_pip','phone_number','buying_type','address', 'status','total_price','date']
	list_filter = ('buying_type', 'status')
	actions = [make_paid, make_aip, make_ip]
