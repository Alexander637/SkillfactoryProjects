from django.utils.decorators import method_decorator
from .models import Advertisement, Response
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from .forms import AdvertisementForm, ResponseForm, ResponseFilterForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'board/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_advertisements = Advertisement.objects.filter(user=self.request.user)
        responses = Response.objects.filter(advertisement__in=user_advertisements).order_by('-created_at')

        filter_form = ResponseFilterForm(self.request.GET)
        if filter_form.is_valid():
            if filter_form.cleaned_data['advertisement']:
                responses = responses.filter(advertisement=filter_form.cleaned_data['advertisement'])

        selected_advertisement = self.request.GET.get('advertisement')
        context['selected_advertisement'] = selected_advertisement
        context['user_advertisements'] = user_advertisements
        context['responses'] = responses
        context['filter_form'] = filter_form
        return context

    def post(self, request, *args, **kwargs):
        if 'accept' in request.POST:
            response = get_object_or_404(Response, pk=request.POST.get('response_id'))
            if not response.accepted:
                response.accepted = True
                response.save()
                response.accepted = True
                response.save()

                subject = 'Your response has been accepted'
                message = f'Hi {response.user.username},\n\nYour response to the advertisement "{response.advertisement.title}" has been accepted.'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [response.user.email]

                send_mail(subject, message, from_email, recipient_list)

        elif 'delete' in request.POST:
            response = get_object_or_404(Response, pk=request.POST.get('response_id'))
            response.delete()
        return self.get(request, *args, **kwargs)


class AdvertisementList(ListView):
    model = Advertisement
    template_name = 'board/advertisement_list.html'
    queryset = Advertisement.objects.order_by('-created_at')
    context_object_name = 'advertisements'


class AdvertisementDetailView(DetailView):
    model = Advertisement
    template_name = 'board/advertisement_detail.html'
    context_object_name = 'advertisement'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = Response.objects.filter(advertisement=self.object)
        context['response_form'] = ResponseForm()
        return context


class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm
    template_name = 'board/response_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.advertisement = get_object_or_404(Advertisement, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('advertisement_detail', kwargs={'pk': self.kwargs['pk']})


class ResponseDeleteView(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'board/response_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('advertisement_detail', kwargs={'pk': self.object.advertisement.pk})


class AdvertisementTypeMixin(LoginRequiredMixin):
    form_class = AdvertisementForm
    model = Advertisement
    template_name = 'board/advertisement_edit.html'
    success_url = reverse_lazy('advertisements')

    def form_invalid(self, form):
        errors = form.errors

        for field in errors:
            if 'Ensure this value has at most' in str(errors[field]):
                value = form[field].value()
                truncated_value = value[:128]
                form.add_error(field, f'Сократите до: {truncated_value}')

        return super().form_invalid(form)


class AdvertisementCreateView(AdvertisementTypeMixin, CreateView):

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdvertisementUpdateView(AdvertisementTypeMixin, UpdateView):
    def get_queryset(self):
        return Advertisement.objects.filter(user=self.request.user)


class AdvertisementDeleteView(AdvertisementTypeMixin, DeleteView):
    template_name = 'board/advertisement_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_message'] = 'Are you sure you want to delete this advertisement?'

        return context
