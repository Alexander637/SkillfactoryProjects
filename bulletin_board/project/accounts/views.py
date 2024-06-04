from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.contrib.auth import login
from django.views.generic import View
from .forms import SignUpForm
from board.models import User, Profile
from django.conf import settings
from django.utils import timezone
from django.utils.html import strip_tags


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            profile = Profile.objects.create(user=user)
            profile.activation_token_expires = timezone.now() + timezone.timedelta(
                days=settings.ACTIVATION_LINK_EXPIRATION_DAYS)
            profile.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            text_content = strip_tags(message)
            email = EmailMultiAlternatives(mail_subject, text_content, settings.EMAIL_HOST_USER, [form.cleaned_data['email']])
            email.attach_alternative(message, "text/html")
            email.send()

            return render(request, 'accounts/confirmation_sent.html')
        return render(request, 'accounts/signup.html', {'form': form})


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            profile = Profile.objects.get(user=user)
            if profile.activation_token_expires is None or profile.activation_token_expires > timezone.now():
                user.is_active = True
                user.save()
                login(request, user)
                return render(request, 'accounts/activation_success.html')
            else:
                return render(request, 'accounts/activation_invalid.html')
        else:
            return render(request, 'accounts/activation_invalid.html')
