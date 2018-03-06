from django.shortcuts import render
from adm.models import Product, Order


# Create your views here.
def products(request):
    products = Product.objects.all()
    return render(request, 'front/products.html', {'products': products})

def order(request):
    orders = Order.objects.all()
    return render(request, 'front/order.html', {'orders': orders})