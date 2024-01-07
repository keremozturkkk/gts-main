from django import template

register = template.Library()

@register.filter
def comma(value):
    return "{:,}".format(value)