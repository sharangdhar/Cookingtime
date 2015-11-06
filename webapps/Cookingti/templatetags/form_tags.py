# -*- coding: utf-8 -*-

from django import template
register = template.Library()

@register.filter
def stars_to_uni(field, args=None):
    if type(field) is not int:
        return None
        
    string = ""
    
    for i in range(field):
        string += "★"
    
    for i in range(5 - field):
        string += "☆"
    
    return string