from django import template
import json

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def cart_total(cart):
    if not cart:
        return 0

    try:
        cart = json.loads(cart)
    except (json.JSONDecodeError, TypeError):
        return 0

    total = 0
    for product_id, details in cart.items():
        total += int(details['quantity']) * float(details['price'])
    return total