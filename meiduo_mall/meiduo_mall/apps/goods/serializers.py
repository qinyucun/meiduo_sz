from rest_framework import serializers
from .models import SKU


class SKUSerializers(serializers.ModelSerializer):
    """
    商品
    """

    class Meta:
        model = SKU
        fields = ['id', 'name', 'price', 'default_image_url', 'comments']
