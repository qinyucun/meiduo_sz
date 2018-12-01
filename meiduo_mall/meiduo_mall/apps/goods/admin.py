from django.contrib import admin
from . import models


# Register your models here.


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
        from celery_tasks.html.tasks import generate_static_list_search_html
        generate_static_list_search_html.delay()

    def delete_model(self, request, obj):
        """
        监听事件
        :param request:
        :param obj:
        :return:
        """
        obj.delete()
        from celery_tasks.html.tasks import generate_static_list_search_html
        generate_static_list_search_html.delay()


admin.site.register(models.GoodsCategory, GoodsCategoryAdmin)
admin.site.register(models.GoodsChannel)
admin.site.register(models.Goods)
admin.site.register(models.Brand)
admin.site.register(models.GoodsSpecification)
admin.site.register(models.SpecificationOption)
admin.site.register(models.SKU)
admin.site.register(models.SKUSpecification)
admin.site.register(models.SKUImage)
