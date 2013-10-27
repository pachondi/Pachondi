from django import template
from app.users.utils import date_in_words
register = template.Library()

@register.filter
def display_date_in_words(date):
    return date_in_words(date)

@register.filter    
def comments(post):
    return post.postcomment_set.all()
