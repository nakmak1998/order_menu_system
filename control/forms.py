from django import forms
from control.models import OrderItem, Order, ProductType


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'

    def clean(self):
        cleaned_data = super(OrderItemForm, self).clean()
        # TODO: если продукты из одной категоории, то выбросить ошибку
        products = cleaned_data['products']
        pruduct_types = ProductType.objects.all()
        not_valid_products = []
        for p_type in pruduct_types:
            count = 0
            for p in products:
                if p.type == p_type:
                    count += 1
            if count > 1:
                not_valid_products.append((p_type, count))
        if not_valid_products:
            raise forms.ValidationError(
                f"Нельзя добавить два и более блюд одного типа"
            )
        return cleaned_data



class OrderForm(forms.ModelForm):
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = '__all__'

