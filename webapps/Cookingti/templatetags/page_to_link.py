# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter
def page_to_links(field, args=None):
    if field == "food"
		return "recipe"
	else
		return "food"