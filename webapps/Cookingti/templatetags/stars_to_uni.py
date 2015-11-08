# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter
def stars_to_uni(field, args=None):
    if field == None:
        return "☆☆☆☆☆"
        
    try:
        field = int(field)
    except:
        return ""
    
    string = ""
    
    for i in range(field):
        string += "★"
    
    for i in range(5 - field):
        string += "☆"
    
    return string