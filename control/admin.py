from django.contrib import admin
from control import models
from control import forms
from datetime import date, timedelta


class AdminSite(admin.AdminSite):
    site_header = 'Система контроля питания'
    site_title = "Администрирование системой"
    index_title = "Администрирование системой"


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    max_num = 3
    exclude = ('is_done',)

    def get_formset(self, request, obj=None, **kwargs):
        kwargs['form'] = forms.OrderItemForm
        return super(OrderItemInline, self).get_formset(request, obj, **kwargs)


class Order(admin.ModelAdmin):
    inlines = (OrderItemInline,)
    list_display = ('date', 'military_id')
    list_filter = ('date',)

    class Media:
        js = ("control/js/order.js",)

    def changelist_view(self, request, extra_context=None):
        if request.user.has_perm('control.add_menustructure'):
            extra_context = self.get_mealpoint_purchase_data()
        if request.user.has_perm('control.add_order'):
            extra_context = self.get_mealpoint_control_data()
        return super(Order, self).changelist_view(request, extra_context)

    def get_mealpoint_purchase_data(self):
        today = date.today()
        next_monday = date.today() + timedelta(days=7 - today.weekday())
        next_sunday = next_monday + timedelta(days=7)
        next_week_orderitems = models.OrderItem.objects.filter(order__date__gte=next_monday).filter(
            order__date__lte=next_sunday)
        return {
            'table_content': next_week_orderitems.values('products__name').annotate(models.models.Count('products')),
            'table_title': f"Общее количество заказов на следующую неделю ({next_monday} - {next_sunday})"
        }

    def get_mealpoint_control_data(self):
        return {
            'meal_control_data': [{
                'military_name': 'Иван Рубец',
                'breakfast': True,
                'lunch': True,
                'dinner': True
            }]}

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


class MilitaryAdmin(admin.ModelAdmin):
    list_filter = ('company__name',)


admin_site = AdminSite(name='Пункт раздачи питания')

admin_site.register(models.Company)
admin_site.register(models.Order, Order)
admin_site.register(models.Menu, MenuInline)
admin_site.register(models.Military, MilitaryAdmin)
admin_site.register(models.ProductType)
admin_site.register(models.Product)
