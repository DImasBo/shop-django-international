"""svetlyachokshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.i18n import i18n_patterns

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('lang/<str:code>/',views.select_lang,name='set_language'),
#    path('filer/', include('filer.urls')),
    path('add/product/<int:product_id>',views.add_to_cart,name='add_to_cart_url'),
    path('minus/product/<int:product_id>',views.minus_to_cart,name='minus_to_cart_url'),
    path('remove/product/<int:product_id>',views.remove_from_cart,name='remove_from_cart_url'),
]

urlpatterns += i18n_patterns(
	path('',views.IndexView.as_view(), name='index'),
    path('callback/',views.callback_view,name='callback_url'),
    path('cart/',views.CartView.as_view(),name='cart_url'),
    path('finish/order/', views.OrderFinish.as_view(),name="order_finish_url"),
    path('set/order/',views.CreateOrder.as_view(),name='create_order_url'),
    path('category/<str:category>/',views.ProductListView.as_view(),name="product_category_url"),
    path('page/<str:slug>/',views.PageViews.as_view(),name="page_url"),
    path('product/<str:slug>/',views.ProductViews.as_view(),name='product_url'),
    prefix_default_language=False,	
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
