from django.shortcuts import render

from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import ContextMixin

from django.conf import settings
from django.core.mail import send_mail

from django.utils.http import is_safe_url
from django.urls import translate_url
# from django.http.response import HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.conf import settings
from django.utils import translation
from cart.cart import Cart
from .models import Product, ProductImage
from .models import Category, Page,  Question, Order
from .forms import FormQuestion
from django.views.generic.edit import CreateView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

# language
def select_lang(request, code):
	go_next = request.META.get('HTTP_REFERER', '/')
	go_next = go_next.replace('en/','').replace('ru/','').replace('uk/','')
	response = HttpResponseRedirect(go_next)
	if code and translation.check_for_language(code):
		next_trans = translate_url(go_next, code)
		if next_trans != go_next:
			response = HttpResponseRedirect(next_trans)
		if hasattr(request, 'session'):
			request.session[LANGUAGE_SESSION_KEY] = code,
			response.set_cookie(
				settings.LANGUAGE_COOKIE_NAME, code,
				max_age=settings.LANGUAGE_COOKIE_AGE,
				path=settings.LANGUAGE_COOKIE_PATH,
				domain=settings.LANGUAGE_COOKIE_DOMAIN,
				)
	return response

# content
class BaseVeiwMixin(ContextMixin):

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		pages = Page.objects.filter(is_publish=True)
		try:
			context['description_site'] = pages.get(slug='description-site')
		except ObjectDoesNotExist:
			print("ERROR: Does not create  'description-site' page")
		context['menu_pages'] = pages.filter(is_menu=True)
		context['categories'] = Category.objects.all()
		context['cart'] = Cart(self.request)
		context['callback_form'] = FormQuestion()
		return context

class ProductListView(ListView,BaseVeiwMixin):
	model = Product
	paginate_by	= 10

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		category = Category.objects.get(slug = self.kwargs.get('category'))
		context['category_name'] = category.name
		context['category_id'] = category.id
		return context

class IndexView(TemplateView,BaseVeiwMixin):
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		products = Product.objects.filter(is_publish=True)
		categories_index = []
		for category in context['categories']:
			p = products.filter(category=category)
			if len(p) > 0:
				c = {
					'name':category.name,
					'products':p[:3]
				}
				categories_index.append(c)
		context['categories_index'] = categories_index
		return context

class PageViews(DetailView,BaseVeiwMixin):
	model = Page

class ProductViews(DetailView,BaseVeiwMixin):
	model = Product


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['product_album'] = ProductImage.objects.filter(product=context['product'])
		return context
# order veiws
class CreateOrder(BaseVeiwMixin,CreateView):
	model = Order
	fields = ['second_name','first_name','last_name','phone_number','email','buying_type','address','comments']
	def send_order(self, order):
		email = settings.EMAIL_HOST_USER
		message = '''Клієт {} {} {} оформив замовлення.<br>
Перетелефонуйте для уточнення деталей.
Сума: {}<br>
Номер: {}<br>c
<a href="https://svetlyachokshop.com/admin/svetlyachokshop/order/{}/change/">переглянути </a>'''.format(order.second_name, order.first_name, order.last_name, order.total_price, order.phone_number, order.id)
		tema = 'Замовлення !!!'
		try:
			send_mail(tema, message, email, [email] ,html_message=message, fail_silently=False)
		except:
			print('email error!!!!!!!!!!!!!!!!!!!!!!!!!')

	def form_valid(self, form):
		cart = Cart(self.request)
		cart.cart.checked_out = True
		cart.cart.save()
		form.instance.cart = cart.cart
		form.instance.total_price = cart.summary()
		response = super().form_valid(form)
		self.send_order(form.instance)
		return response

class OrderFinish(TemplateView,BaseVeiwMixin):
	template_name = 'svetlyachokshop/order_finish.html'

# views cart

def add_to_cart(request, product_id):
	product = Product.objects.get(id=product_id)
	cart = Cart(request)
	cart.add(product, product.price)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def minus_to_cart(request,product_id):
	product = Product.objects.get(id=product_id)
	cart = Cart(request)
	cart.minus(product,product.price)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def remove_from_cart(request, product_id):
	product = Product.objects.get(id=product_id)
	cart = Cart(request)
	cart.remove(product)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class CartView(TemplateView,BaseVeiwMixin):
	template_name = 'cart.html'

def callback_view(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		email_ = request.POST.get('email')
		question = request.POST.get('question')
		q = Question(name=name, email=email_, question=question)
		q.save()

		email = settings.EMAIL_HOST_USER
		message = '''Запитання від {} .<br>
email: {}<br>
Запитання:
{}
'''.format(name,email_,question)
		tema = 'Запитання !!!'
		try:
			send_mail(tema, message, email, [email] ,html_message=message, fail_silently=False)
		except:
			print('email error!!!!!!!!!!!!!!!!!!!!!!!!!')

	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# search view
class SearchList(ListView,BaseVeiwMixin):
	model = Product
	paginate_by	= 10
	def get_queryset(self):
		search = self.request.GET['search']
		return Product.objects.filter(Q(translation__title__icontains=search) | Q(translation__description__icontains=search))
