from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from ecomapp.models import Category, Product, Cart, CartItem, ProductImage, Order, Page
from django.core.paginator import Paginator

from django.http.response import HttpResponseRedirect
from ecomapp.forms import  OrderForm, PageEditForm, OrderForm, CategoryForm

from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin 
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def get_cart(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.item.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	return cart

class BaseView(TemplateView):
	template_name = 'ecomapp/index.html'
	
	def get(self, request):
		cart = get_cart(request)	
		categories = Category.objects.all() 
		pages = Page.objects.all()[:3]
		description = Page.objects.get(slug='description')
		about_us = Page.objects.get(slug='about-us')
		contacts = Page.objects.get(slug='contacts')
		buying_type = Page.objects.get(slug='buying-type')
		#try:
		#except Exception as e:
	#		description = Page.objects.get_or_create(title='Опис',description='опис панелі сайту знизу',slug='description')
		
		self.context = {
			'categories': categories,
			'cart':cart,
			'pages':pages,
			'description':description,
			'buying_type':buying_type,
			'about_us':about_us,
			'contacts':contacts,
		}
		return render(request,self.template_name,context=self.context)

class OrderDetailView(BaseView):

	template_name = 'ecomapp/order_detail.html'
	def get(self, request,id):
		super().get(request)
		order = Order.objects.get(id=id)
		self.context['form'] = OrderForm(instance = order)
		self.context['order'] = order
		return render(request,self.template_name,context=self.context)

class PageView(BaseView):

	template_name = 'ecomapp/page.html'

	def get(self,request,slug):
		super().get(request)
		self.context['page'] = Page.objects.get(slug=slug)
		return render(request, self.template_name, context=self.context)

class PageEdit(LoginRequiredMixin,BaseView):
	template_name = 'ecomapp/page_edit.html'
	
	raise_exception = True

	def get(self, request,slug):
		super().get(request)
		page = Page.objects.get(slug=slug)
		self.context['form'] = PageEditForm(instance = page)
		self.context['page'] = page
		return render(request,self.template_name,context=self.context)

	def post(self,request,slug):
		super().get(request)
		self.context['page'] = Page.objects.get(slug=slug)
		bound_form = PageEditForm(request.POST, instance=self.context['page'])
		self.context['form'] = bound_form
		if bound_form.is_valid():
			form = bound_form.save()
			return redirect(reverse('page_url', kwargs={'slug':form.slug}))
		return render(request,self.template_name,context=self.context)

class IndexView(BaseView):

	def get(self,request):
		super().get(request)
		products = Product.objects.filter(available=True)
		#масив для вюшки з категорією на головній і її продуктами
		categories_index = []
		for category in self.context['categories']:
			p = products.filter(category=category)
			if len(p) > 0:
				c = {
					'name':category.name,
					'url':category.get_absolute_url(),
					'products':p[:3]
				}
				categories_index.append(c)
		self.context['categories_index'] = categories_index
		return render(request,self.template_name,context=self.context)

class SearchView(BaseView):

	template_name = 'ecomapp/product_list.html'
	def get(self,request):
		super().get(request)
		search_query = request.GET.get('search', '')
		if search_query == '':
			return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
		self.context['category'] = Category()
		self.context['category'].name = 'Пошук: ' + search_query
		products = Product.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query) )
		paginator = Paginator(products, 9)
		page_number = request.GET.get('page', 1)
		page = paginator.get_page(page_number)
		self.context['page'] = page
		return render(request,self.template_name,context=self.context)

class CategoryView(BaseView):

	template_name = 'ecomapp/product_list.html'
	def get(self,request,slug):
		super().get(request)		
		self.context['category'] = self.context['categories'].get(slug=slug)
		self.context['category'].name = 'Категорія: ' + self.context['category'].name 
		products = Product.objects.filter(category=self.context['category'])
		paginator = Paginator(products, 9)
		page_number = request.GET.get('page', 1)
		page = paginator.get_page(page_number)
		self.context['page'] = page
		self.context['is_paginated'] = page.has_other_pages()


		if page.has_previous():
			self.context['prev_url'] = '?page={}'.format(page.previous_page_number())
		else:
			self.context['prev_url'] = False

		if page.has_next():
			self.context['next_url'] = '?page={}'.format(page.next_page_number())
		else:
			self.context['next_url'] = False
		return render(request, self.template_name ,context=self.context)

class CategoriesEditView(LoginRequiredMixin,BaseView):
	template_name = 'ecomapp/edit_categories.html'
	
	raise_exception = True

	def get(self,request):
		super().get(request)
		self.context['form'] = CategoryForm()
		return render(request,self.template_name,context=self.context)

	def post(self,request):
		super().get(request)
		self.context['form'] = CategoryForm()
		bound_form = CategoryForm(request.POST)
		if bound_form.is_valid():
			form = bound_form.save()
			self.context['categories'] = Category.objects.all()
			return render(request,self.template_name,context=self.context)			
		return render(request,self.template_name,context=self.context)		

class ProductDetailView(BaseView):

	template_name = 'ecomapp/product_detail.html'
	def get(self,request,slug):
		super().get(request)		
		self.context['product'] = Product.objects.get(slug=slug)
		self.context['product_album'] = ProductImage.objects.filter(product=self.context['product'])
		return render(request, self.template_name ,context=self.context)

class CartView(BaseView):

	template_name = 'ecomapp/cart.html'


class ListOrder(BaseView):

	template_name = 'ecomapp/orders.html'

	def get(self, request):
		super().get(request)
		orders = Order.objects.all()
		self.context['orders'] = orders
		return render(request, self.template_name, context=self.context )


class CreateOrder(BaseView):


	template_name = 'ecomapp/order.html'
	
	def send_order(self, order):
		email = settings.EMAIL_HOST_USER
		message = '''{} {} {}<br>
Сума: {}<br>
Номер: {}<br>
<a href="#">переглянути </a>'''.format(order.second_name, order.first_name, order.last_name, order.total, order.phone_number)

		tema = 'Замовлення !!!'
		send_mail(tema, message, email, [email],html_message=message, fail_silently=False)

	def get(self,request):
		super().get(request)		
		self.context['form'] = OrderForm()
		return render(request, self.template_name, context=self.context )

	def post(self,request):
		super().get(request)
		bound_form = OrderForm(request.POST)
		if bound_form.is_valid():
			form = bound_form.save(commit=False)
			form.total = self.context['cart'].cart_total
			form.products_add(self.context['cart'])
			form.save()
			try:
				self.send_order(form)
			except:
				print("not network")
			return redirect(reverse('order_finish_url'))

		self.context['form'] = bound_form 
		return render(request, self.template_name, context=self.context )

class OrderFinish(BaseView):

	template_name = 'ecomapp/order_finish.html'

def add_to_cart(request, slug):
	cart = get_cart(request)
	order = Order()
	cart.add_to_cart(slug)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def remove_from_view(request, slug):
	cart = get_cart(request)
	cart.remove_from_cart(slug)
	return redirect(reverse('cart_url'))

def remove_from_order_view(request,id, item_id):
	cart = get_cart(request)
	order = Order.objects.get(id=id)
	order.remove_from_order(item_id)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))