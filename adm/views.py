from django.contrib.auth.models import User
from .models import Product, Order
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import re
import os
from django.db import IntegrityError
from django.core.mail import EmailMessage
from shaurman import settings

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

# Imaginary function to handle an uploaded file.
# Create your views here.

def users(request):
    users = User.objects.all()
    return render(request, 'adm/users.html', {'users': users})

def products(request):
    products = Product.objects.all()
    return render(request, 'adm/products.html', {'products': products})

def orders(request):
    orders = Order.objects.all()
    return render(request, 'adm/orders.html', {'orders': orders})

def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        file_str = [line.rstrip('\n') for line in fs.open(filename, 'r')]
        os.remove(os.path.join(settings.MEDIA_ROOT,str(filename)))
        status_dict = []
        for file_line in file_str:
            user_str = file_line.split(',')
            try:
                if EMAIL_REGEX.match(user_str[2]):
                    try:
                        password = User.objects.make_random_password()
                        user = User.objects.create_user(user_str[2], user_str[2], password)
                        user.first_name = user_str[0]
                        user.last_name = user_str[1]
                        user.save()
                        email = EmailMessage('Registration at shaurman', 'Registration at shaurman is complete. Your Username is {} Your password is {}'.format(user_str[2], password), to=[user_str[2]])
                        email.send()
                    except IntegrityError:
                        status_dict.append(user_str[2] + " user is exist")
            except IndexError:
                status_dict.append(file_line + " bad line format")
        if len(status_dict) > 0:
            return render(request, 'adm/upload.html', {'errors': status_dict})
        return render(request, 'adm/upload.html', {
            'successes': "all users added successful"
        })
    return render(request, 'adm/upload.html')
