from django import template

register = template.Library()

@register.filter
def stars_to_uni(field, args=None):
    if type(field) is not str:
        return
        
    string = "☆☆☆☆☆"
    
    for i in range field:
        string[i] = "★"
    
    return string