from django import template
from django.utils.html import mark_safe
from html.parser import HTMLParser
from bs4 import BeautifulSoup

register = template.Library()


class TruncateHTMLParser(HTMLParser):
    def __init__(self, max_length):
        super().__init__()
        self.max_length = max_length
        self.result = []
        self.current_length = 0
        self.truncated = False
        self.tag_stack = []

    def handle_starttag(self, tag, attrs):
        if self.current_length < self.max_length:
            attrs_str = ''.join(f' {k}="{v}"' for k, v in attrs)
            self.result.append(f'<{tag}{attrs_str}>')
            self.tag_stack.append(tag)

    def handle_endtag(self, tag):
        if self.current_length < self.max_length:
            self.result.append(f'</{tag}>')
            self.tag_stack.pop()

    def handle_data(self, data):
        if self.current_length < self.max_length:
            remaining_length = self.max_length - self.current_length
            if len(data) > remaining_length:
                self.result.append(data[:remaining_length])
                self.current_length += remaining_length
                self.truncated = True
            else:
                self.result.append(data)
                self.current_length += len(data)
        else:
            self.truncated = True

    def get_truncated_html(self):
        while self.tag_stack:
            self.result.append(f'...</{self.tag_stack.pop()}>')
        return ''.join(self.result)


@register.filter
def safe_truncate_html(value, length):
    parser = TruncateHTMLParser(length)
    parser.feed(value)
    truncated_html = parser.get_truncated_html()
    return mark_safe(truncated_html)


@register.filter
def remove_images_from_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    for img in soup.find_all('img'):
        img.extract()
    return str(soup)
