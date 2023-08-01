from decimal import Decimal
from django.conf import settings
from .models import Product

CART_SESSION_KEY = getattr(settings, 'CART_SESSION_KEY', 'cart')

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.save()

    def get_cart_items(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_items = []

        for product in products:
            cart_items.append({
                'product': product,
                'quantity': self.cart[str(product.id)]['quantity'],
                'price': Decimal(self.cart[str(product.id)]['price']),
                'total_price': Decimal(self.cart[str(product.id)]['price']) * self.cart[str(product.id)]['quantity']
            })

        return cart_items

    def get_total_price(self):
        total = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        return total