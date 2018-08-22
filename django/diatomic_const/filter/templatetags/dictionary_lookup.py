from django.template.defaulttags import register
from django import template


@register.filter
def get_item(d, key):
    return d.get(str(key))



  

