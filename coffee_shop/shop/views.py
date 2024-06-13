from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
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
    return render(request, 'shop/view_cart.html', {'cart': cart})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('product_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'shop/register.html', {'form': form})
