from django.contrib.auth.models import User
from .models import Product, Order
from django.shortcuts import render, reverse
from django.core.urlresolvers import reverse_lazy
from django.core.files.storage import FileSystemStorage
import re
import os
from django.db import IntegrityError
from django.core.mail import EmailMessage
from shaurman import settings
from django.views.generic.edit import FormMixin
from django.views.generic import ListView
from adm.forms import ProductForm
from django.http import Http404
from django.views.generic import DeleteView
from django.utils.datastructures import MultiValueDictKeyError

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def users(request):
    users = User.objects.all()
    return render(request, 'adm/users.html', {'users': users})


class FormListView(FormMixin, ListView):

    def get_success_url(self):
        return reverse('admin_products')

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404((u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        return Product.objects.all()


class ProductView(FormListView):
    model = Product
    form_class = ProductForm
    template_name = 'adm/products.html'

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
        return super().post(request, *args, **kwargs)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('adm:admin_products')


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('adm:admin_orders')


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('adm:users')


class ListProduct(ListView):
    model = Product
    template_name = 'adm/products.html'


def orders(request):
    orders = Order.objects.all()
    return render(request, 'adm/orders.html', {'orders': orders})


def upload(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            file_str = [line.rstrip('\n') for line in fs.open(filename, 'r')]
            os.remove(os.path.join(settings.MEDIA_ROOT, str(filename)))
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
                            email = EmailMessage('Registration at shaurman',
                                                 'Registration at shaurman is complete. Your Username is {} Your password is {}'.format(
                                                     user_str[2], password), to=[user_str[2]])
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
    except MultiValueDictKeyError:
        pass
    return render(request, 'adm/upload.html')
