"""shaurman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from adm import views
from django.contrib.auth.decorators import login_required

app_name = 'adm'

urlpatterns = [
    url(r'^users/?$', login_required(views.users), name="users"),
    url(r'^user/(?P<pk>\d+)/?$', login_required(views.UserDeleteView.as_view()), name="user_delete"),
    url(r'^products/?$', login_required(views.ProductView.as_view()), name="admin_products"),
    url(r'^orders/?$', login_required(views.orders), name="admin_orders"),
    url(r'^order/(?P<pk>\d+)/?$', login_required(views.OrderDeleteView.as_view()), name="order_delete"),
    url(r'^import/?$', login_required(views.upload), name="import"),
    url(r'^product/(?P<pk>\d+)/?$', login_required(views.ProductDeleteView.as_view()), name="product_delete"),
]
