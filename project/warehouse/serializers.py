from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .models import Company, OrderProduct, Product, WarehouseManager, Warehouse


class WarehouseManagerSerializer(serializers.ModelSerializer):

    class Meta:
        model = WarehouseManager
        fields = "__all__"


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'product_name',
            'count',
        ]


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'product_name',
            'count',
            'company',
        ]

    def create(self, validated_data, **kwargs):
        product_id = validated_data.get('product_name')
        company_id =validated_data.get('company')

        if not Product.objects.filter(product_name=product_id, company=company_id):
            product_obj = Product.objects.create(**validated_data)
            data = {} 

            if product_obj:
                    data['product'] = product_obj
                    data['count'] = product_obj.count
                    data['status'] = "Add"
                    OrderProduct.objects.create(**data)
                    return validated_data        
        else:
            self.update(self, product_id, company_id)
        return validated_data

    def update(self, instance, product_id, company_id):
        product_obj = Product.objects.filter(product_name=product_id, company=company_id).first()
        if product_obj:
            data = {} 
            data['product'] = product_obj
            data['count'] = instance._validated_data.get('count')
            data['status'] = "Add"
            OrderProduct.objects.create(**data)

            product_obj.count += instance._validated_data.get('count')
            product_obj.save()            
            return Response(status=status.HTTP_201_CREATED)
        

class OrderProductSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderProduct
        fields = [
            'city',
            'product_name',
            'count',
            'created_at', 
            'status',  
        ]

    def get_city(self, obj):            
        product_id = Product.objects.filter(id=obj.product_id).first()
        try:
            company_id = Company.objects.filter(id=product_id.company_id).first()
            if company_id:
                return company_id.city
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def get_product_name(self, obj):            
        product_id = Product.objects.filter(id=obj.product_id).first()
        return product_id.product_name
    

class CompanyOwnerSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(many=True)
    
    class Meta:
        model = Company
        fields = [
            'company_name',
            'product',
        ]
    

class CompanyViewSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(many=True)

    class Meta:
        model = Company
        fields = [
            'city',
            'product',
        ]
            

class WarehouseSerializer(serializers.ModelSerializer):
    companies = CompanyOwnerSerializer(many=True)

    class Meta:
        model = Warehouse
        fields = [
            'city',
            'companies',
        ]
