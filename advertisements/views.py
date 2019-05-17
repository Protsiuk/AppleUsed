from django.shortcuts import get_object_or_404, HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.core.mail import EmailMessage

from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic.edit import FormMixin
from django.utils import timezone
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from advertisements.forms import AdvertisementCreationForm, AdvertisementImageFormSet
from advertisements.models import Advertisement, AdvertisementFollowing, PageHit
from chat.forms import UserMessageForm, GuestMessageForm
from chat.models import Message, Chat


class AdvertisementHomeView(ListView):
    model = Advertisement
    success_url = '/advertisements/chat-list/'
    template_name = 'main.html'

    def get_queryset(self):
        qs = Advertisement.objects.order_by('-created').filter(is_active=True, is_visible=True)[:4]
        return qs


class AdvertisementsSearchView(ListView):
    model = Advertisement
    model_2 = AdvertisementFollowing
    template_name = 'search_list.html'
    paginate_by = 15

    def get_queryset(self):
        query = self.request.GET.get('q')
        result = Advertisement.objects.search(query).filter(is_visible=True)
        from_min_price = self.request.GET.get('min_price')
        to_max_price = self.request.GET.get('max_price')
        if from_min_price:
            result = result.filter(price__gte=from_min_price)
        if to_max_price:
            result = result.filter(price__lte=to_max_price)
        ordering = self.request.GET.get('ordering')
        if ordering:
            ordering = self.request.GET.get('ordering')
        else:
            ordering = '-created'
        return result.order_by(ordering)

    def get_context_data(self, **kwargs):
        context = super(AdvertisementsSearchView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['following_ads'] = self.model.objects.filter(favorites__user=self.request.user)
        return context


class MyAdvertisementActiveView(LoginRequiredMixin, ListView):
    model = Advertisement
    template_name = 'my_active_advertisements.html'

    def get_queryset(self):
        ctx = super(MyAdvertisementActiveView, self).get_queryset()
        author = self.request.user
        ctx = ctx.filter(author=author, is_active=True).order_by('-created')
        return ctx


class MyAdvertisementArchiveView(LoginRequiredMixin, ListView):
    model = Advertisement
    template_name = 'archive_advertisements.html'

    def get_queryset(self):
        ctx = super(MyAdvertisementArchiveView, self).get_queryset()
        author = self.request.user
        ctx = ctx.filter(author=author, is_active=False).order_by('-created')
        return ctx


class AdvertisementsListMarksView(LoginRequiredMixin, ListView):
    model = Advertisement
    template_name = 'favorites.html'
    model_following = AdvertisementFollowing
    paginate_by = 15

    def get_queryset(self):
        qs = self.model.objects.filter(favorites__user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super(AdvertisementsListMarksView, self).get_context_data(**kwargs)
        following_ads = self.model.objects.filter(favorites__user=self.request.user)
        context['following_ads'] = following_ads
        context['count_following_ads'] = len(following_ads)
        return context


class AdvertisementCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Advertisement
    success_url = '/advertisements/'
    form_class = AdvertisementCreationForm
    template_name = 'create_advertisement.html'
    success_message = 'Ваше сообщение будет опубликовано после одобрения модератором!'

    """Create NEW advertisement"""

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_form = AdvertisementImageFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  image_form=image_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_form = AdvertisementImageFormSet(request.POST, request.FILES)#, queryset=AdvertisementImage.objects.none())
        if (form.is_valid() and image_form.is_valid()):
            return self.form_valid(form, image_form)
        else:
            return self.form_invalid(form, image_form)

    def form_valid(self, form, image_form):
        """
        Called if all forms are valid. Creates a Advertisement instance along with
        associated AdvertisementImage (ImageFormsets Images) and then redirects to a
        success page.
        """
        form.instance.author = self.request.user
        self.object = form.save()
        image_form.instance = self.object
        image_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, image_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  image_form=image_form))

    def get_context_data(self, **kwargs):
        context = super(AdvertisementCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['advertisementimage_form'] = AdvertisementImageFormSet(self.request.POST)
        else:
            context['advertisementimage_form'] = AdvertisementImageFormSet()
        return context


class AdvertisementUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Advertisement
    success_url = '/advertisements/my_active_advertisements/'
    form_class = AdvertisementCreationForm
    template_name = 'update_advertisement.html'
    success_message = 'Ваше сообщение будет опубликовано после одобрения модератором!'

    """Update existing advertisement"""

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_form = AdvertisementImageFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  image_form=image_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_form = AdvertisementImageFormSet(request.POST, request.FILES, instance=self.object)
        if (form.is_valid() and image_form.is_valid()):
            return self.form_valid(form, image_form)
        else:
            return self.form_invalid(form, image_form)

    def form_valid(self, form, image_form):
        """
        Called if all forms are valid. Updates a Advertisement instance along with
        associated AdvertisementImage (ImageFormsets Images) and then redirects to a
        success page.
        """
        self.object = form.save(commit=False)
        self.object.is_visible = False
        self.object.is_moderated = False
        self.object.updated = timezone.now()
        self.object = form.save()
        image_form.instance = self.object
        image_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, image_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  image_form=image_form))

    def get_context_data(self, **kwargs):
        context = super(AdvertisementUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset_image'] = AdvertisementImageFormSet(self.request.POST, instance=self.object)
        else:
            context['formset_image'] = AdvertisementImageFormSet(instance=self.object)
        return context


# it's use
class AjaxAPIAdmarkView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None, format=None):
        """
        Return True and url to icon favorites True if hadn't a relation.
        """
        user = self.request.user
        admark, created = AdvertisementFollowing.objects.get_or_create(user=user, advertisement_id=self.kwargs['pk'])
        url_ = admark.get_absolute_url()
        if not created:
            admark.delete()
            data = {
                'ad_mark': False,
                'url_favorite_icon': '/static/img/favorite_FALSE.png'
                    }
        else:
            data = {
                'ad_mark': True,
                'url_favorite_icon': '/static/img/favorite_TRUE.png'
            }
        return Response(data)


class AdvertisementDetailView(SuccessMessageMixin, FormMixin, DetailView):
    model = Advertisement
    form_class = UserMessageForm
    form_class_2 = GuestMessageForm
    model_hits = PageHit
    model_following = AdvertisementFollowing
    template_name = 'advertisement_detail.html'
    success_message = 'Ваше сообщение отправлено!'

    def get_success_url(self):
        return reverse('advertisement_detail', kwargs={'pk': self.kwargs['pk']})

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        if self.request.user.is_authenticated:
            form_class = self.form_class
        else:
            form_class = self.form_class_2
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(AdvertisementDetailView, self).get_context_data(**kwargs)
        advertisement = get_object_or_404(Advertisement, pk=self.kwargs['pk'])
        user = self.request.user
        context['img_following'] = self.following(user, advertisement)
        context['form'] = self.get_form()
        views_page = self.hit_count(user, advertisement)
        context['views_page'] = views_page
        if user == advertisement.author:
            context['you_is_author'] = True
        return context

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        Called if form is valid. Create a NEW message in current dialog or create NEW dialog and then redirects to a
        success page (current dialog).
        """
        new_message = form.save(commit=False)
        new_message.subject_ad = get_object_or_404(self.model, id=self.kwargs['pk'])
        new_message.receiver_msg = new_message.subject_ad.author
        if self.request.user.is_authenticated:
            new_message.sender_msg = self.request.user
        try:
            if self.request.user.is_authenticated:
                chat_id = Message.objects.filter(sender_msg=new_message.sender_msg,
                                                 receiver_msg=new_message.receiver_msg,
                                                 subject_ad=new_message.subject_ad).values('chat_id')
            else:
                chat_id = Message.objects.filter(temporary_user_email=new_message.temporary_user_email,
                                                 receiver_msg=new_message.receiver_msg,
                                                 subject_ad=new_message.subject_ad).values('chat_id')
            new_message.chat = Chat.objects.get(id=chat_id)
        except ObjectDoesNotExist:
            new_message.chat = Chat.objects.create()
        new_message = form.save()
        chat = Chat.objects.get(pk=new_message.chat.id)
        chat.last_send_message = new_message
        chat.save()
        self.send_mail_to_receiver(receiver=new_message.receiver_msg, subject=new_message.subject_ad.title)
        return super(AdvertisementDetailView, self).form_valid(form)

    def form_invalid(self, form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(self.get_context_data(form=form))


    def hit_count(self, user, advertisement):
        """
        Counter for views pages
        If user is not author counter increment +1
        """
        if user != advertisement.author:
            hit_count, created = self.model_hits.objects.get_or_create(advertisement=advertisement)
            if created:
                hit_count.hits_counter = 1
            else:
                hit_count.hits_counter += 1
            hit_count.save()
            views = hit_count.hits_counter
        else:
            try:
                views_ad = self.model_hits.objects.get(advertisement=advertisement)
                views = views_ad.hits_counter
            except self.model_hits.DoesNotExist:
                views = 0
        return views

    def following(self, user, advertisement):
        """
        Add or remove page to favorites list
        Create relate current user to current ad if hasn't before, or remove if it had.
        """
        try:
            follow = AdvertisementFollowing.objects.get(user=user, advertisement=advertisement)
            following = '/static/img/favorite_TRUE.png'
        except AdvertisementFollowing.DoesNotExist:
            following = '/static/img/favorite_FALSE.png'
        return following

    def send_mail_to_receiver(self, receiver, subject):
        current_site = get_current_site(self.request)
        domen = current_site.domain
        subject_msg = 'Вы получили ответ на объявление '+subject
        receiver = receiver.email
        body = 'Вы получили новое сообщение по '+subject+'\n перейдите по адресу '+self.get_success_url()
        email_message = EmailMessage(subject=subject_msg, body=body, to=[receiver])
        email_message.send()
        return 'ok'


class AdvertisementDeleteView(LoginRequiredMixin, DeleteView):
    model = Advertisement
    success_url = reverse_lazy('main')
    template_name = 'advertisement_delete.html'

    def get_object(self, queryset=None):
        advertisement = get_object_or_404(Advertisement, pk=self.kwargs['pk'])
        return advertisement

    def get_success_url(self):
        return reverse_lazy('search_list')


class AdvertisementDeactivateView(LoginRequiredMixin, DeleteView):
    model = Advertisement
    success_url = reverse_lazy('main')
    template_name = 'advertisement_deactivate.html'

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse_lazy('archive_advertisements')
