from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Response


@receiver(post_save, sender=Response)
def notify_advertisement_owner(sender, instance, created, **kwargs):
    if created:
        advertisement = instance.advertisement
        owner = advertisement.user

        subject = 'Your advertisement has a new response'
        message = (f'Hi {owner.username},\n\nYour advertisement "{advertisement.title}"'
                   f' has received a new response from {instance.user.username}.')
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [owner.email]

        send_mail(subject, message, from_email, recipient_list)
