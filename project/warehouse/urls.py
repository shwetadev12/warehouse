from django.urls import include, path
from warehouse import views

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('warehouse/',
         views.warehouse_list_view,
         name='warehouse_list_view'),
    path('product/',
         views.company_list_view,
         name='product_list_view'),
    path('product-add/<int:pk>',
         views.product_add_view,
         name='product_debit'),
    path('product-debit/<int:pk>',
         views.product_deduct_view,
         name='product_debit'),
    path('company/',
         views.product_api_view,
         name='company_view'),
    path('product-order/',
         views.product_order_list_view,
         name='product_orders_list_view'),
    
]