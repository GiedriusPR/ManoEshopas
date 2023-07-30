from django.contrib.auth.forms import AuthenticationForm
from .models import Category, Product, Customer, ProductOrder, Review, Orders, User_login
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm, CartForm
from django.contrib.auth.decorators import login_required
import logging
from django.core.paginator import Paginator
from .forms import UserUpdateForm, ProfileUpdateForm
from django.views import View
import json
from .templatetags.myfilters import cart_total

logger = logging.getLogger(__name__)

def index(request):
    products = Product.objects.all()
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
        'products': page_obj,
        'categories': categories,
        'cart_items': products_in_cart,
        'total_cart_value': total_cart_value,
        'user': request.user,
    }

    return render(request, 'index.html', context)

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
                return redirect('index')  # Replace 'index' with the name of your homepage URL pattern
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="eshopas_app/login.html", context={"login_form": form})


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
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'profile.html', context)

class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'category_list.html', context)

@login_required
def cart_detail(request):
    cart_items = request.session.get('cart_items', [])
    products_in_cart = Product.objects.filter(id__in=cart_items)
    total_cart_value = sum([product.price for product in products_in_cart])

    return render(request, 'cart_detail.html', {'products': products_in_cart, 'total_cart_value': total_cart_value})

    cart_items = []

    for product_id, details in cart.items():
        product = get_product_by_id(product_id)
        if product:
            item = {
                'product': product,
                'quantity': details.get('quantity', 0),
                'price': details.get('price', 0),
                'total': int(details.get('quantity', 0)) * float(details.get('price', 0))
            }
            cart_items.append(item)

    context = {
        'cart_items': cart_items,
        'total_cart_value': cart_total(cart)
    }

    return render(request, 'cart_detail.html', context)

def get_product_by_id(product_id):
    pass


def add_to_cart(request, product_id):
    # Your existing logic to get the product and add it to the cart
    # For example:
    product = get_object_or_404(Product, id=product_id)
    if product is None:
        # Handle the case where the product does not exist
        return redirect('product_not_found')

    # Assuming you have a 'cart' variable that represents the cart data
    # Your logic to add the product to the cart
    cart = request.session.get('cart', {})  # Get the current cart or create an empty one if it doesn't exist
    cart[product_id] = {
        'name': product.name,
        'price': str(product.price),  # Convert the price to a string to avoid JSON serialization issues
        'quantity': 1,  # Or update the quantity if the product already exists in the cart
    }

    # Serialize the cart data to JSON before setting it in the session
    request.session['cart'] = json.dumps(cart)

    return redirect('cart_detail')  # Redirect to the cart_detail page after adding the item

