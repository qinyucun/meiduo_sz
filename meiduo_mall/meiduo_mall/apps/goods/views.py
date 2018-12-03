from django.shortcuts import render

# Create your views here.
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter

from goods.models import SKU
from .serializers import SKUSerializers, SKUIndexSerializer


class SKUListView(ListAPIView):
    """
    sku序列化器
    """
    # 排序的方法
    filter_backends = (OrderingFilter,)
    ordering_fields = ('create_time', 'price', 'sales')
    # 指定序列化器
    serializer_class = SKUSerializers

    # 指定查询集
    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return SKU.objects.filter(category_id=category_id, is_launched=True)


class SKUSearchViewSet(HaystackViewSet):
    """
    SKU搜索
    """
    index_models = [SKU]

    serializer_class = SKUIndexSerializer
