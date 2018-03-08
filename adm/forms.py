from django.forms import ModelForm
from adm.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'restaurant', 'price']
