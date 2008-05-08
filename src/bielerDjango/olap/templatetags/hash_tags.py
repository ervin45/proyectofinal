from django import template
register = template.Library()

@register.filter
def hash(h, key):
    return h[key]

@register.filter
def hash2(h, key):
    print "HHHHHHHHHHHASSSSSSS", h, key
    return h[key]

@register.filter
def hash3(h, key):
    print "HHHHHHHHHHHASSSSSSS", h, key
    return h[key]

@register.filter
def hash4(h, key):
    print "HHHHHHHHHHHASSSSSSS", h, key
    return h[key]

@register.filter
def sub(h, index):
    return h[index]

@register.filter
def size(h):
    return len(h)

