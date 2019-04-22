from django import template


register = template.Library()


@register.filter
def remove_p(value):
    return value.replace('<p>', '').replace('</p>', '')
