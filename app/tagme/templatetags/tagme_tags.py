from django import template
from app.tagme.forms import TagField, TagWidget

register = template.Library()

@register.simple_tag 
def render_tags():
    all_tags = "All tags for this discussion should come nyah"
    return TagWidget
