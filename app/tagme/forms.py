from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext as _
from django.utils import six

from app.tagme.utils import tag_parser


class TagWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        return super(TagWidget, self).render(name, value, attrs)

class TagField(forms.CharField):
    widget = TagWidget

    def clean(self, value):
        value = super(TagField, self).clean(value)
        try:
            return tag_parser(value)
        except ValueError:
            raise forms.ValidationError(_("Please provide a comma-separated list of tags."))