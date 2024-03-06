from django import template
import re

register = template.Library()

CENSOR_WORDS = ['bad', 'amiss', 'some']


@register.filter()
def censor(value):
    for word in CENSOR_WORDS:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        value = pattern.sub(lambda x: '*' * len(x.group()), value)

    return value


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
