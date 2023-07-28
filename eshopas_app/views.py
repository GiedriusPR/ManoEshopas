from django.contrib.auth.forms import AuthenticationForm
from .models import Category, Product, Customer, ProductOrder, Review, Orders, User_login
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm, CartForm
from django.contrib.auth.decorators import login_required
import logging
from django.core.paginator import Paginator


logger = logging.getLogger(__name__)

def index(request):
    products = Product.objects.all()  # Show all products
    categories = Category.objects.all()

    # Get cart information
    cart_items = request.session.get('cart_items', [])
    products_in_cart = Product.objects.filter(id__in=cart_items)
    total_cart_value = sum([product.price for product in products_in_cart])

    # Pagination
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,  # Use 'products' instead of 'featured_products'
        'categories': categories,
        'cart_items': products_in_cart,
        'total_cart_value': total_cart_value,
        'user': request.user,
    }

    return render(request, 'index.html', context)  # Send the 'context' variable, not just the user


def category(request):
    categories = Category.objects.all()
    return render(request, 'category.html', {'categories': categories})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)
    return render(request, 'category_detail.html', {'category': category, 'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def cart(request):
    cart_items = request.session.get('cart_items', [])
    products = Product.objects.filter(id__in=cart_items)

    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            product = get_object_or_404(Product, id=product_id)

            cart_items.append(product.id)
            request.session['cart_items'] = cart_items

            # Redirect to the cart page after adding the item
            return redirect('cart')
    else:
        form = CartForm()

    return render(request, 'cart.html', {'form': form, 'products': products})

@login_required
def checkout_view(request):
    # Add logic here to handle the checkout process
    # For example, calculate the total price, create orders, and process payment
    if request.method == 'POST':
        # Handle the form submission for checkout
        # Process the order and redirect to order success page
        pass  # Replace this with your logic for order processing

    return render(request, 'checkout.html')

def order_success(request, order_id):
    order = get_object_or_404(Orders, id=order_id)

    # Add logic here to display order details and confirmation message

    return render(request, 'order_success.html', {'order': order})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('index')  # Replace 'home' with the name of your homepage URL pattern
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="eshopas_app/login.html", context={"login_form":form})


def logout_view(request):
    logout(request)
    return redirect('index')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def product_list(request):
    try:
        products = Product.objects.all()
        logger.info(f'product_list view called, found {len(products)} products')
    except Exception as e:
        logger.error(f'Error fetching products: {e}')
        products = []

    return render(request, 'products.html', {'products': products})

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})
