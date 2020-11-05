from django.contrib import admin
from control import models
from control import forms
import re


class AdminSite(admin.AdminSite):
    site_header = 'Система контроля питания'
    site_title = "Администрирование системой"
    index_title = "Администрирование системой"
    pass


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    max_num = 3

    def get_formset(self, request, obj=None, **kwargs):
        kwargs['form'] = forms.OrderItemForm
        return super(OrderItemInline, self).get_formset(request, obj, **kwargs)


class Order(admin.ModelAdmin):
    inlines = (OrderItemInline,)
    list_display = ('date', 'military_id')
    list_filter = ('date',)

    class Media:
        js = ("order.js",)

    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs['form'] = forms.OrderForm
        return super(Order, self).get_form(request, obj, **kwargs)

    def get_fields(self, request, obj=None):
        return super(Order, self).get_fields(request, obj)


class MenuStructure(admin.TabularInline):
    model = models.MenuStructure
    extra = 0


class MenuInline(admin.ModelAdmin):
    inlines = (MenuStructure,)


admin_site = AdminSite(name='control')

admin_site.register(models.Company)
admin_site.register(models.Order, Order)
admin_site.register(models.Menu, MenuInline)
admin_site.register(models.Military)
admin_site.register(models.ProductType)
admin_site.register(models.Product)
