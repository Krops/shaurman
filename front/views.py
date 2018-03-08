from django.shortcuts import render, redirect
from adm.models import Product, Order
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout


def products(request):
    products = Product.objects.all()
    return render(request, 'front/products.html', {'products': products})


@login_required
def order(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'front/order.html', {'orders': orders})


@login_required
def add_order(request, pk, amount):
    if request.method == 'POST':
        order = Order(user=request.user, product=Product.objects.get(pk=pk), date=timezone.now(), amount=amount)
        order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def signin(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('products')
        else:
            return render(request, 'front/login.html', {'error': 'Passwords or user didn\'t match'})
    else:
        return render(request, 'front/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('products')
