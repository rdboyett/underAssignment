from random import randint

from django import template

register = template.Library()


@register.assignment_tag(takes_context=False)
def random_number():
    return randint(1, 25)



@register.filter
def totalPrice(price, quantity):
    return "%.2f" % float(float(price)*quantity)