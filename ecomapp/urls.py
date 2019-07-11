from django.urls import path, include
from ecomapp import views

urlpatterns = [
	path('',views.IndexView.as_view(), name='index'),
	path('search/',views.SearchView.as_view(), name = 'search'),
	path('page/<str:slug>', views.PageView.as_view() , name='page_url'),
	path('page_edit/<str:slug>', views.PageEdit.as_view() , name='page_edit_url'),
	path('cart/', views.CartView.as_view(),name='cart_url'),
	path('order/', views.CreateOrder.as_view(),name='create_order_url'),
	
	path('order/<int:id>', views.OrderDetailView.as_view(),name='order_detail_url'),
	path('orders/', views.ListOrder.as_view(),name='order_list_url'),
	path('order_finish/',views.OrderFinish.as_view(), name='order_finish_url'),
	path('add_to_cart/<str:slug>',views.add_to_cart,name='add_to_cart_url'),
	path('remove_from_view/<str:slug>',views.remove_from_view,name='remove_from_view_url'),
	path('remove_from_order/<int:id>/<int:item_id>',views.remove_from_order_view,name='remove_from_order_url'),
	path('category/<str:slug>',views.CategoryView.as_view(), name='category_list_url' ),
	path('product/<str:slug>', views.ProductDetailView.as_view(),name='product_detail_url'),
	path('edit_categories/',views.CategoriesEditView.as_view(),name='edit_categories_url'),
]