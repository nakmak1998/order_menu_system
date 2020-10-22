from django.contrib import admin
from control import models


class AdminSite(admin.AdminSite):
    site_header = 'Система контроля питания'
    site_title = "Администрирование системой"
    index_title = "Администрирование системой"

    pass


admin_site = AdminSite(name='control')


class OrderChoicesAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    exclude = ('is_done',)
    filter_horizontal = ('products',)
    list_filter = ('military_id__company__name', 'date')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        menu_structure = models.MenuStructure.objects.first()
        kwargs["queryset"] = menu_structure.products.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin_site.register(models.Order, OrderChoicesAdmin)
admin_site.register(models.Company)
admin_site.register(models.Military)
admin_site.register(models.ProductType)
admin_site.register(models.Product)
admin_site.register(models.MenuStructure)
