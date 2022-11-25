from django import forms

from stripe_app.models import Order, Item


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["items"]

    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), widget=forms.CheckboxSelectMultiple)

