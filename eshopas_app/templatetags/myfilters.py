from django import template
import json


register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def multiply(value, arg):
    return value * arg


# @register.filter(name='cart_total_quantity')
# def cart_total_quantity(cart):
#     total_quantity = sum(item['quantity'] for item in cart)
#     return total_quantity
