from django.contrib import admin
from . import models

from celery_tasks.html.tasks import generate_static_list_search_html, generate_static_sku_detail_html


# Register your models here.
class SKUAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """
        监听事件
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        obj.save()

        generate_static_sku_detail_html.delay(obj.id)


class SKUSpecificationAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """
        监听事件
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        sku = obj.sku
        if not sku.default_image_url:  #判断有没有默认图片
            sku.default_image_url = obj.image.url
        obj.save()

        generate_static_sku_detail_html.delay(obj.id)

    def delete_model(self, request, obj):
        """
        监听事件
        :param request:
        :param obj:
        :return:
        """
        obj.delete()

        generate_static_sku_detail_html.delay(obj.id)


class GoodsCategoryAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """
        监听事件
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        obj.save()

        generate_static_list_search_html.delay()

    def delete_model(self, request, obj):
        """
        监听事件
        :param request:
        :param obj:
        :return:
        """
        obj.delete()

        generate_static_list_search_html.delay()


admin.site.register(models.GoodsCategory, GoodsCategoryAdmin)
admin.site.register(models.GoodsChannel)
admin.site.register(models.Goods)
admin.site.register(models.Brand)
admin.site.register(models.GoodsSpecification)
admin.site.register(models.SpecificationOption)
admin.site.register(models.SKU,SKUAdmin)
admin.site.register(models.SKUSpecification)
admin.site.register(models.SKUImage,SKUSpecificationAdmin)
