from django import template
from ..models import MEDIA_MAPPING
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg

@register.filter(name='get_media_name')
def get_media_name(media_number):
    # Use the MEDIA_MAPPING dictionary to get the media name
    return MEDIA_MAPPING.get(media_number, "Unknown Media")

@register.filter(name='highlight_keywords')
def highlight_keywords(value, keywords):
    """
    Highlight keywords in the given text.

    Usage:
    {{ text|highlight_keywords:"keyword1,keyword2,keyword3" }}
    """
    
    # Split the comma-separated keywords into a list
    keyword_list = [kw.strip() for kw in keywords.split(',')]

    # Iterate over each keyword and wrap it with a span tag for highlighting
    for keyword in keyword_list:
        value = value.replace(keyword, f'<span class="keyword highlighted-keyword">{escape(keyword)}</span>')

    return value