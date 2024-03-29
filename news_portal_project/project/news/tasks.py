from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from .models import Post, Category
import datetime


def my_data_send(date_value, title_text):
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=date_value)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True)

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts
        }
    )
    msg = EmailMultiAlternatives(
        subject=title_text,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_on_monday():
    date_value = 7
    title_text = 'Посты за неделю'

    my_data_send(date_value, title_text)


@shared_task
def send_every_morning():
    date_value = 1
    title_text = 'Посты за сутки'
    my_data_send(date_value, title_text)
    