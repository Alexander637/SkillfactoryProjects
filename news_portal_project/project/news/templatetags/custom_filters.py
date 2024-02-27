from django import template
import re

register = template.Library()

CENSOR_WORDS = ['bad', 'some', 'amiss', 'title']


@register.filter()
def censor(value):
    for word in CENSOR_WORDS:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        value = pattern.sub(lambda x: '*' * len(x.group()), value)

    return value
