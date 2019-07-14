from django.db import models

from django.shortcuts import reverse

from django.utils.text import slugify
from transliterate import translit

from django.core.validators import MaxValueValidator, MinValueValidator

from decimal import Decimal
# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=50, verbose_name = 'Назва')
	slug = models.SlugField(blank=True,verbose_name="Ключове слово(не обов'ясково)")

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('category_list_url',kwargs={'slug':self.slug})

	def save(self, *args, **kwargs):
		if not self.slug and self.name:
			slug = slugify(translit(self.name,'uk', reversed=True))
			self.slug = slug
		super().save( *args, **kwargs)

	class Meta:
		verbose_name = 'Категорію'
		verbose_name_plural = 'Категорії'
		ordering = ['name']
		
class Page(models.Model):

	title = models.CharField(max_length=100, verbose_name='Заголовок')
	description = models.TextField(verbose_name='Опис')
	slug = models.SlugField(verbose_name="Ключове слово")

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('page_url', kwargs={'slug':self.slug})

	def get_edit_url(self):
		return reverse('page_edit_url', kwargs={'slug':self.slug})

	class Meta:
		verbose_name_plural = 'Сторінки сайта'
		verbose_name = 'Сторінку сайта'

def image_folder(instance, filename):
	filename = instance.slug + '.' + filename.split('.')[1]
	return "{0}/{1}".format(instance.slug,filename)

def image_folder_cover(instance, filename):
	filename = instance.slug + '_cover.' + filename.split('.')[-1]
	return "{0}/{1}".format(instance.slug,filename)

def image_folder_album(instance, filename):
	filename = instance.product.slug + '.' + filename.split('.')[-1]
	return "{0}/{1}".format(instance.product.slug, filename)

class Product(models.Model):

	title = models.CharField(max_length=50, verbose_name='Заголовок')
	description = models.TextField( verbose_name='Опис')
	price = models.DecimalField(max_digits=9, decimal_places=2,  verbose_name='Ціна')
	category = models.ForeignKey(Category,on_delete=models.CASCADE, verbose_name='Категорія')
	count = models.PositiveIntegerField(default=1,  verbose_name='Кількість товару')
	slug = models.SlugField(blank=True,  verbose_name="Ключове слово(не обов'ясково)")
	available = models.BooleanField(default=True, verbose_name='В наявності')
	date = models.DateTimeField(auto_now_add=True)
	album_cover = models.ImageField(upload_to=image_folder_cover, verbose_name='Фото обкладинки')

	def get_absolute_url(self):
		return reverse('product_detail_url',kwargs={'slug':self.slug})

	def delete(self, *args, **kwargs):
		self.album_cover.delete(save=False)
		super().delete(args, kwargs)

	def save(self, *args, **kwargs):
		if not self.slug and self.title:
			slug = slugify(translit(self.title,'uk', reversed=True))
			self.slug = slug
		super().save( *args, **kwargs)

	def get_add_to_cart_url(self):
		return reverse('add_to_cart_url',kwargs={'slug':self.slug})

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Продукт'
		verbose_name_plural = 'Продукти'
		ordering = ['-date']

class Reduction(models.Model):

	title = models.CharField(max_length = 100)
	reduction = models.PositiveSmallIntegerField(default = 1, validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])
	description = models.TextField()
	product = models.ManyToManyField(Product)
	image = models.ImageField(upload_to=image_folder, blank=True, null=True)

	date = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return "{0}% | {1}".format(str(self.reduction), self.title)

	class Meta:
		verbose_name = 'Знишку'
		verbose_name_plural = 'Знишки'
		ordering = ['-date']

class ProductImage(models.Model):
	
	product = models.ForeignKey(Product, related_name='images',on_delete=models.CASCADE)
	images = models.ImageField(upload_to=image_folder_album )

	def __str__(self):
		return self.images.url

	def delete(self, *args, **kwargs):
		self.images.delete(save=False)
		super().delete(*args,**kwargs)

	class Meta:
		verbose_name = 'фото'
		verbose_name_plural = 'фото'

class CartItem(models.Model):

	product = models.ForeignKey(Product,on_delete=models.CASCADE)
	qty = models.PositiveIntegerField(default=1)
	item_total = models.DecimalField(max_digits=9,decimal_places=2,default=0)

	def __str__(self):
		return "Cart item for product {0}".format(self.product.title)

class Cart(models.Model):

	item = models.ManyToManyField(CartItem, blank=True)
	cart_total = models.DecimalField(max_digits=9,decimal_places=2,default=0)

	def __str__(self):
		return str(self.id)

	def add_to_cart(self,slug):
		product = Product.objects.get(slug=slug)
		new_item = CartItem.objects.get_or_create(product=product,item_total=product.price)[0]
		print(new_item)
		if new_item not in self.item.all():
			self.item.add(new_item)
			self.save()
		self.sum_items()

	def get_qty(self):
		return str(self.item.count())

	def remove_from_cart(self,slug):
		product = Product.objects.get(slug=slug)
		for item in self.item.all():
			if item.product == product:
				self.item.remove(item)
				self.save()
		self.sum_items()	

	def sum_items(self):
		total_price = Decimal(0.00)
		for item in self.item.all():
			total_price = total_price + item.item_total
		self.cart_total = total_price
		self.save()

class Order(models.Model):
# Accepted in processing = AIP_status, 'Прийнятий в обробку'
# In processing = IP_status, 'В обробці'
# Paid = PAID_status, 'Оплачено'

	ORDER_STATUS_CHOICES = (
		('AIP_status', 'Прийнятий в обробку'),
		('IP_status', 'В обробці'),
		('PAID_status', 'Оплачено'),
	)

	DELIVERY_STATUS = (
		('nova_poshta', 'Нова пошта'),
		('ukr_poshta', 'Укр-пошта'),
	)
	# cart = models.ForeignKey(Cart,on_delete=models.CASCADE, verbose_name='Корзина')
	products = models.ManyToManyField(CartItem, verbose_name='Товари')
	total = models.DecimalField(max_digits=9, decimal_places=2, default = 0, verbose_name='Сума')
	second_name = models.CharField(max_length=200, verbose_name='Прізвище')
	first_name = models.CharField(max_length=200, verbose_name='Імя')
	last_name = models.CharField(max_length=200, verbose_name='Побатькові')
	phone_number = models.CharField(max_length=9, verbose_name='Номер телефону +380')
	email = models.EmailField(blank = True, verbose_name='Електрона пошта')
	buying_type = models.CharField(max_length=40,choices=DELIVERY_STATUS, verbose_name='Спосіб доставки')
	address = models.CharField(max_length=255, verbose_name='адреса')
	status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES,default='AIP_status', verbose_name='Статус')
	comments = models.TextField(blank = True, verbose_name='Коментарь')
	date = models.DateTimeField(auto_now_add=True)

	def remove_from_order(self,item_id):
		C_item = CartItem.objects.get(id=item_id)
		for item in self.products.all():
			if item == C_item:
				self.products.remove(item)
				self.save()
		self.sum_items()	

	def sum_items(self):
		total_price = Decimal(0.00)
		for item in self.products.all():
			total_price = total_price + item.item_total
		self.total = total_price
		self.save()

	def products_add(self,cart):
		self.save()
		for item in cart.item.all():
			print(item)
			self.products.add(item.id)
		self.save()
		cart.delete()

	def __str__(self):
		return "{} /ДАТА: {} /ПІБ: {} {} {}".format(str(self.id), str(self.date.strftime("%d-%B-%Y")), self.second_name,self.first_name, self.last_name)

	def get_absolute_url(self):
		return reverse('create_order_url',kwargs={'id':self.id})

	class Meta:
		ordering = ['-date']
		verbose_name = 'Замовлення'
		verbose_name_plural = 'Замовлення'