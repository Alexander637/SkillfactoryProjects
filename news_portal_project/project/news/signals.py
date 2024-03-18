from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory
from django.conf import settings

SITE_URL = settings.SITE_URL
DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL


def send_notifications(preview, pk, title, subscribers, category_type):
    if category_type == 'NW':
        link = f'{SITE_URL}/news/{pk}'
    elif category_type == 'AR':
        link = f'{SITE_URL}/articles/{pk}'

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': link
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(post_save, sender=PostCategory)
def notify_about_new_post(sender, instance, created, **kwargs):
    if created:
        post = instance.postThrough
        category = instance.categoryThrough
        category_type = post.categoryType
        subscribers = list(category.subscribers.values_list('email', flat=True))

        send_notifications(post.preview(), post.pk, post.title, subscribers, category_type)
