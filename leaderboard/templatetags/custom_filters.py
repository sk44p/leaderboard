from django import template
import re

register = template.Library()

@register.filter
def is_media_path(value):
    # Check if the value matches 'media/' or '/media/'
    if re.match(r'^/?media/', value):
        return True
    return False
