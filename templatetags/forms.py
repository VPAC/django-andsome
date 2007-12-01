from django.template import Library
from django.conf import settings

register = Library()

@register.inclusion_tag('formfield.html')
def formfield(field):
    return {'field': field, }

@register.inclusion_tag('inlineformfield.html')
def inlineformfield(field1, field2, field3=False):
    return locals()

@register.inclusion_tag('checkbox_formfield.html')
def checkbox_formfield(field):
    return {'field': field, }

@register.inclusion_tag('form_as_div.html')
def form_as_div(form):
    return {'form': form, }

@register.inclusion_tag('search_form.html')
def search_form(url='', terms=''):
    return { 'url': url, 'terms': terms, 'MEDIA_URL': settings.MEDIA_URL }
