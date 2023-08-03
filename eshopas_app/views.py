from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.views import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
import logging
from .models import (
    Category, Product, Cart, Customer, ProductOrder, Review, Orders, User_login, ProductComment, CartItem
)
from .forms import (
    UserRegistrationForm, CartForm, UserUpdateForm, ProfileUpdateForm, ProductCommentForm
)
from .templatetags.myfilters import cart_total
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import model_to_dict
from _decimal import Decimal

logger = logging.getLogger(__name__)

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Get cart information
    cart_items = request.session.get('cart_items', [])
    products_in_cart = Product.objects.filter(id__in=cart_items)
    total_cart_value = sum([product.price for product in products_in_cart])

    # Pagination
    paginator = Paginator(products, 21)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': categories,
        'cart_items_count': len(cart_items),  # Update the cart count here
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


def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'category_detail.html', {'category': category, 'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    comments = ProductComment.objects.filter(product=product)
    form = ProductCommentForm()

    return render(request, 'product_detail.html', {'product': product, 'comments': comments, 'form': form})

@login_required
def cart(request):
    cart = Cart(request)
    cart_items = cart.get_cart_items()
    total_price = cart.get_total_price()

    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            product = get_object_or_404(Product, id=product_id)
            cart.add(product)
            # Redirect to the cart page after adding the item
            return redirect('cart')

    else:
        form = CartForm()

    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)

@login_required()
def cart_count(request):
    cart_items = request.session.get('cart_items', [])
    return JsonResponse({'count': len(cart_items)})


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
                return redirect('login')  # Replace 'index' with the name of your homepage URL pattern
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, template_name="registration/login.html", context={"login_form": form})


def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print("Form is valid:", form.cleaned_data)
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
        else:
            print("Form errors:", form.errors)
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
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profile.html', context)

class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'category_list.html', context)


@login_required
def cart_detail(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)

    total_cart_value = sum(item.total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_cart_value': total_cart_value,
    }

    return render(request, 'cart_detail.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Item added to your cart!")
    return redirect('cart_detail')


@login_required
def get_product_by_id(product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        product = None
    return product


@login_required
def add_comment(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductCommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            user = request.user
            ProductComment.objects.create(product=product, user=user, comment=comment)
            return redirect('product_detail', product_id=product_id)
    else:
        form = ProductCommentForm()

    return render(request, 'add_comment.html', {'form': form})


@require_POST
@login_required
def update_quantity(request, product_id):
    if request.method == 'POST':
        new_quantity = int(request.POST['quantity'])
        if new_quantity <= 0:
            messages.warning(request, "Quantity must be a positive number.")
        else:
            cart = get_object_or_404(Cart, user=request.user)
            cart.update_quantity(product_id, new_quantity)
            messages.success(request, "Quantity updated successfully.")
    return redirect('cart_detail')


@require_POST
@login_required
def remove_item(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()
    messages.success(request, "Item removed from your cart.")
    return redirect('cart_detail')


def search(request):
    query = request.GET.get('query')

    if query:
        search_results = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        search_results = []

    context = {
        'query': query,
        'products': search_results,
    }

    return render(request, 'search.html', context)


@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the product is already in the user's favorites
    if request.user in product.favorites.all():
        # If yes, remove it
        product.favorites.remove(request.user)
    else:
        # If not, add it
        product.favorites.add(request.user)

    return redirect('product_detail', product_id=product_id)


@login_required
def my_favorites_view(request):
    user = request.user
    if user.is_authenticated:
        favorite_products = user.favorites.all()
    else:
        favorite_products = []

    context = {
        'favorite_products': favorite_products
    }
    return render(request, 'my_favorites.html', context)
