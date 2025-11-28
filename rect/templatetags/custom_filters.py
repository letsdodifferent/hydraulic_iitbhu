from django import template

register = template.Library()

@register.filter
def range_filter(value):
    """Generates a range of numbers."""
    return range(1, value + 1)