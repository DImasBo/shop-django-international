from django.db import models

from django.shortcuts import reverse

from django.utils.text import slugify
from transliterate import translit
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from django.template.defaultfilters import slugify

from django.core.validators import MaxValueValidator, MinValueValidator

from decimal import Decimal

from parler.models import TranslatableModel, TranslatedFields

from cart.models import Cart


def image_folder_cover(instance, filename):
	filename = instance.slug + '_cover.' + filename.split('.')[-1]
	return "{0}/{1}".format(instance.slug,filename)

def image_folder_album(instance, filename):
	filename = instance.product.slug + '.' + filename.split('.')[-1]
	return "{0}/{1}".format(instance.product.slug, filename)

class Category(TranslatableModel):
	translation = TranslatedFields(
		name = models.CharField(max_length=50, verbose_name = 'Назва')
	)
	slug = models.SlugField(unique=True,blank=True,verbose_name="Слово для Сайту")

	def save(self, *args, **kwargs):
		if not self.slug and self.name:
			slug = slugify(translit(self.name,'uk', reversed=True))
			self.slug = slug
		super().save( *args, **kwargs)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('product_category_url',kwargs={'category':self.slug})

	class Meta:
		verbose_name = 'Категорію'
		verbose_name_plural = 'Категорії'

class Page(TranslatableModel):
	translation = TranslatedFields(
		title = models.CharField(max_length=100, verbose_name='Заголовок'),
		description = models.TextField(verbose_name='Опис'),
		meta_description = models.TextField(null=True,blank=True,verbose_name="Мета опис"),
		meta_keywords = models.CharField(null=True,max_length=255,blank=True,verbose_name="Мета Ключові слова")
	)
	is_publish = models.BooleanField(default=True, verbose_name='показувати на сайті')
	is_menu = models.BooleanField(default=True,blank=True,verbose_name="Додати в панель меню?")
	slug = models.SlugField(verbose_name="Ключове слово")

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('page_url', kwargs={'slug':self.slug})

	class Meta:
		verbose_name_plural = 'Сторінки сайта'
		verbose_name = 'Сторінку сайта'

@python_2_unicode_compatible
class Product(TranslatableModel):

	STATUS = (
		("av", _("В наявності")),
		("not_av", _("нема в наявності")),
		("order", _("Під замовлення")),
		)

	translation = TranslatedFields(
		title = models.CharField(max_length=50, verbose_name='Заголовок'),
		description = models.TextField( verbose_name='Опис'),
		meta_description = models.TextField(null=True,blank=True,verbose_name="Мета опис"),
		meta_keywords = models.CharField(null=True,max_length=255,blank=True,verbose_name="Мета Ключові слова")
	)

	is_publish = models.BooleanField(default=True, verbose_name='показувати на сайті')
	price = models.DecimalField(max_digits=9, decimal_places=2,  verbose_name='Ціна')
	category = models.ForeignKey(Category,on_delete=models.CASCADE, verbose_name='Категорія')
	count = models.PositiveIntegerField(default=1,  verbose_name='Кількість товару')
	slug = models.SlugField(unique=True, blank=True, verbose_name="Слово для Сайту")
	status = models.CharField(choices=STATUS,default=STATUS[0],max_length=20,verbose_name= "Варіанти")
	date = models.DateTimeField(auto_now_add=True)
	product_cover = models.ImageField(upload_to=image_folder_cover, verbose_name='Фото обкладинки')

	def save(self, *args, **kwargs):
		if not self.slug and self.title:
			slug = slugify(translit(self.title,'uk', reversed=True))
			self.slug = slug
		super().save( *args, **kwargs)

	def get_status_display(self):
		for item in self.STATUS:
			if item[0] == self.status:
				return item[1]

	def get_absolute_url(self):
		return reverse('product_url',kwargs={'slug':self.slug})

	def delete(self, *args, **kwargs):
		self.album_cover.delete(save=False)
		super().delete(args, kwargs)

	def __str__(self):
		return self.title
	
	def get_minus_url(self):
		return reverse('minus_to_cart_url',kwargs={"product_id":self.id})
    
	def get_add_url(self):        
		return reverse('add_to_cart_url',kwargs={"product_id":self.id})

	class Meta:
		verbose_name = 'Товар'
		verbose_name_plural = 'Товари'
		ordering = ['-date']

class ProductImage(models.Model):	
	product = models.ForeignKey(Product, related_name='image',on_delete=models.CASCADE)
	image = models.ImageField(upload_to=image_folder_album )

	class Meta:
		verbose_name = 'фото'
		verbose_name_plural = 'фото'

#------------ Question ( Callback ) ------------------------------- 

class Question(models.Model):
	name = models.CharField(max_length=100,verbose_name=_("ім'я"))
	email = models.EmailField(verbose_name=_("email"))
	question = models.TextField(verbose_name=_("питання"))
	date = models.DateTimeField(auto_now=True,verbose_name=_("Дата"))

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Запитання"
		verbose_name_plural = "Запитання"

class Order(models.Model):

	ORDER_STATUS_CHOICES = (
		('AIP_status', 'Прийнятий в обробку'),
		('IP_status', 'В обробці'),
		('PAID_status', 'Оплачено'),
	)

	DELIVERY_STATUS = (
		('nova_poshta', _('Нова пошта')),
		('ukr_poshta', _('Укр-пошта')),
	)
	cart = models.ForeignKey(Cart,blank=True,null=True,on_delete=models.CASCADE, verbose_name=_('Корзина'))
	total_price = models.DecimalField(max_digits=9, decimal_places=2, default = 0, verbose_name=_("Сума"),blank=True)
	second_name = models.CharField(max_length=200, verbose_name=_('Прізвище'))
	first_name = models.CharField(max_length=200, verbose_name=_('Імя'))
	last_name = models.CharField(max_length=200, verbose_name=_('Побатькові'))
	phone_number = models.CharField(max_length=9, verbose_name=_('Номер телефону +380'))
	email = models.EmailField(blank = True, null=True, verbose_name=_('Електрона пошта'))
	buying_type = models.CharField(max_length=40,choices=DELIVERY_STATUS, verbose_name=_('Спосіб доставки'))
	address = models.CharField(max_length=255, verbose_name=_('адреса'))
	status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES,default='AIP_status', verbose_name=_('Статус'))
	comments = models.TextField(blank = True, null=True,verbose_name=_('Коментарь'))
	date = models.DateTimeField(auto_now_add=True,verbose_name="Дата")

	def view_pip(self):
		return "{} {} {}".format(self.second_name,self.first_name,self.last_name)
	view_pip.short_description = 'ПІП'

	class Meta:
		verbose_name = "Замовлення"
		verbose_name_plural = "Замовлення"

	def get_absolute_url(self):
		return reverse('order_finish_url')
