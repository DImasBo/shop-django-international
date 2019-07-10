from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Product,ProductImage,Reduction ,Order, Page
from django_summernote.admin import SummernoteModelAdmin

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ ProductImageInline, ]


class PageAdmin(SummernoteModelAdmin):
    summernote_fields = ('description')

# Register your models here.
admin.site.register(Page, PageAdmin)
admin.site.register(Category)
# admin.site.register(Cart)
# admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Reduction)
admin.site.register(Product,ProductAdmin)