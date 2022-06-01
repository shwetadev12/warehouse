from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company, OrderProduct, Product, WarehouseManager, Warehouse
from .serializers import CompanyViewSerializer, OrderProductSerializer, ProductListSerializer, ProductSerializer, WarehouseSerializer
from .permissions import CompanyPermission


class WarehouseAPIView(generics.ListAPIView):
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'name',
        'companies',
    ]
    queryset = Warehouse.objects.all()

    def get_queryset(self):
        if self.request.user.profile_type == 'warehouses_owner':
            return self.queryset.filter()
        if self.request.user.profile_type == 'warehouses_manager':
            warehouse_manager_obj = WarehouseManager.objects.get(manager=self.request.user)
            return Warehouse.objects.filter(id=warehouse_manager_obj.id)

warehouse_list_view = WarehouseAPIView.as_view()

class CompanyAPIView(generics.ListAPIView):
    serializer_class = CompanyViewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'city',
    ]

    def get_queryset(self):
        if self.request.user.profile_type == 'company_owner':
            return Company.objects.filter(owner=self.request.user)

company_list_view = CompanyAPIView.as_view()

class ProductAPIView(generics.ListCreateAPIView, generics.UpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [CompanyPermission]
    queryset = Product.objects.all()
    
product_api_view = ProductAPIView.as_view()


class ProductDeductView(generics.UpdateAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [CompanyPermission]
    queryset = Product.objects.all()

    def update(self, *args, **kwargs):           
        product_count = self.request.data.get('count')
        instance = self.get_object()
        product_obj = Product.objects.filter(id=instance.id).first()
        if product_obj:
            data = {} 
            data['product'] = product_obj
            data['count'] = product_count
            data['status'] = "Deduct"
            OrderProduct.objects.create(**data)

        instance.count -= product_count           
        instance.save()
        result = {
        "message": "Product updated",
        "count": product_obj.count,
        "status": 200,
        }
        return Response(result)

product_deduct_view = ProductDeductView.as_view()


class OrderProductListView(generics.ListAPIView):
    serializer_class = OrderProductSerializer
    permission_classes = [CompanyPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'status',
    ]

    def get_queryset(self):
        company_id = Company.objects.filter(owner=self.request.user).first()
        if company_id:
            product_id = Product.objects.filter(company=company_id.id).first()
            if product_id:
                return OrderProduct.objects.all()                    
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)   

product_order_list_view = OrderProductListView.as_view()           
            

class ProductAddView(generics.UpdateAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [CompanyPermission]
    queryset = Product.objects.all()

    def update(self, request, *args, **kwargs):           
        product_count = self.request.data.get('count')
        instance = self.get_object()
        product_obj = Product.objects.filter(id=instance.id).first()
        if product_obj:
            data = {} 
            data['product'] = product_obj
            data['count'] = product_count
            data['status'] = "Add"
            OrderProduct.objects.create(**data)

        instance.count += product_count           
        instance.save()
        result = {
        "message": "Product updated",
        "count": product_obj.count,
        "status": 200,
        }
        return Response(result)

product_add_view = ProductAddView.as_view()
