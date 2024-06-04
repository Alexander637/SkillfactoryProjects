from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.utils import timezone
from django.conf import settings
from board.models import Advertisement, User
from datetime import timedelta


class Command(BaseCommand):
    help = 'Send newsletter with new advertisements from the last week'

    def handle(self, *args, **kwargs):
        subject = 'Weekly Newsletter'
        message_template = 'board/newsletter_email.html'
        advertisements = Advertisement.objects.filter(created_at__gte=timezone.now() - timedelta(days=7))

        recipient_list = User.objects.filter(is_active=True)
        for user in recipient_list:
            message = render_to_string(message_template, {
                'user': user,
                'advertisements': advertisements
            })
            plain_message = strip_tags(message)
            send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [user.email], html_message=message)

        self.stdout.write(self.style.SUCCESS('Successfully sent newsletter to all users'))
