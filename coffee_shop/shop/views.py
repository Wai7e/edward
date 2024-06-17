import json
import random

from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Product, Cart, CartItem
from .forms import UserRegistrationForm


def product_list(request):
    coffee = Product.objects.filter(category='coffee')
    pastry = Product.objects.filter(category='pastry')
    return render(request, 'shop/product_list.html', {'coffee': coffee, 'pastry': pastry})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('product_list')


@login_required
def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.cartitem_set.all()
    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    order_num = random.randint(1000, 9999)
    return render(request, 'shop/view_cart.html', {'cart': cart, 'cart_total': cart_total, 'order_num': order_num})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                Cart.objects.create(user=user)
                return redirect('product_list')
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] = 'error'
    else:
        form = UserRegistrationForm()
    return render(request, 'shop/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('product_list')


def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    data = json.loads(request.body)
    quantity = data.get('quantity')
    if quantity and quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid quantity'}, status=400)


@require_POST
def delete_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return JsonResponse({'status': 'success'})


def cart_total(request):
    cart = get_object_or_404(Cart, user=request.user)
    total = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
    return JsonResponse({'total': total})
