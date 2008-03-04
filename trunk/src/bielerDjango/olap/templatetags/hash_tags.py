from django import template
register = template.Library()

@register.filter
def hash(h, key):
    return h[key]

@register.filter
def sub(h, index):
    return h[index]

@register.filter
def size(h):
    return len(h)

