from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, HttpResponseRedirect
from moderation.models import Moderation
from moderation.forms import ModerationForm
from advertisements.models import Advertisement
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View, ListView, UpdateView, DetailView, CreateView


class LoginModeratorRequiredMixin(LoginRequiredMixin):

    """
    Abstract CBV mixin that gives access mixins the same customizable
    functionality.
    CBV mixin which verifies that the current user is moderator or superuser authenticated.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_moderator:
            return self.handle_no_permission()
        return super(LoginModeratorRequiredMixin, self).dispatch(request, *args, **kwargs)


class ListForModerateView(LoginModeratorRequiredMixin, ListView):
    model = Moderation
    template_name = 'list_for_moderation.html'
    paginate_by = 1

    def get_queryset(self, **kwargs):
        qs = Advertisement.objects.filter(is_visible=False, is_moderated=False).order_by('-created')
        return qs

    # print(paginate_by)

class MyListModerationView(LoginModeratorRequiredMixin, ListView):

    """Return a list Ads, which request user are moderated."""

    model = Moderation
    template_name = 'my_list_moderation.html'
    paginate_by = 15

    def get_queryset(self, **kwargs):
        # qs = self.model.objects.filter(moderator=self.request.user)
        qs = self.model.objects.filter(moderator=self.request.user).order_by('-end_moderate')
        print(qs)
        return qs


class ModerationAdsView(LoginModeratorRequiredMixin, CreateView):
    model = Moderation
    model2 = Advertisement
    template_name = 'begin_moderation.html'

    def get(self, request, *args, **kwargs):
        self.object = Moderation()
        user = self.request.user
        self.object.moderator = user
        pk = self.kwargs['pk']
        """!!!!!!"""
        print('ad_to_moderation id is -', pk)
        self.object.ad_to_moderate = get_object_or_404(self.model2, pk=pk)
        if not self.object.ad_to_moderate.is_moderated:
            self.object.status = 2
            self.object.save()

            """
            Changed Advertisement's field 'is_moderated' to True.
            """

            self.is_moderated_ad()
            return redirect(self.get_absolute_url(pk=self.object.moderation_id))
        else:
            return reverse('moderation:list_for_moderation')

    def post(self, request, *args, **kwargs):

        """
        Handles POST requests, instantiating a form instance with the passed POST variables and then checking them for
        validity.
        """

        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid() and self.object.status != 2:
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        Called if all forms are valid. Updates a moderation and then redirects to a
        success page.
        """
        self.object = form.save(commit=False)
        self.object.end_moderate = timezone.now()
        self.object = form.save()
        """
        If Ad is approved changed Advertisement's field 'is_visible' to True.
        """
        if self.object.status == 1:
            self.activate_visible_ad()
        return super(ModerationAdsView, self).form_valid(form)

    def activate_visible_ad(self):
        ad = get_object_or_404(self.model2, pk=self.object.ad_to_moderate.id)
        ad.is_visible = True
        ad.save()
        return True

    def get_absolute_url(self, pk):
        return reverse('moderation:moderate_ad', args=(pk,))

    def is_moderated_ad(self):
        ad = get_object_or_404(self.model2, pk=self.object.ad_to_moderate.id)
        ad.is_moderated = True
        ad.save()
        return True





class ModerationBeginView(LoginModeratorRequiredMixin, View):
    model = Moderation
    model2 = Advertisement
    template_name = 'begin_moderation.html'
    # success_message = 'Объявление, уже открыто другим модератором.'

    """Create object of moderation"""

    def get(self, request, *args, **kwargs):
        self.object = Moderation()
        user = self.request.user
        self.object.moderator = user
        pk = self.kwargs['pk']
        """!!!!!!"""
        print('ad_to_moderation id is -', pk)
        self.object.ad_to_moderate = get_object_or_404(self.model2, pk=pk)
        if not self.object.ad_to_moderate.is_moderated:
            self.object.status = 2
            self.object.save()

            """
            Changed Advertisement's field 'is_moderated' to True.
            """

            self.is_moderated_ad()
            return redirect(self.get_absolute_url(pk=self.object.moderation_id))
        else:
            return reverse('moderation:list_for_moderation')

    def get_absolute_url(self, pk):
        return reverse('moderation:moderate_ad', args=(pk,))

    def is_moderated_ad(self):
        ad = get_object_or_404(self.model2, pk=self.object.ad_to_moderate.id)
        ad.is_moderated = True
        ad.save()
        return True


class ModerationFinishedView(LoginModeratorRequiredMixin, UpdateView):
    model = Moderation
    model2 = Advertisement
    success_url = reverse_lazy('moderation:list_for_moderation')
    form_class = ModerationForm
    template_name = 'moderation_ad.html'

    """
    Get created object of moderation
    and checking of Ad and dispatch to view for all off users or rejected
    """

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if self.object.status == 2:
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):

        """
        Handles POST requests, instantiating a form instance with the passed POST variables and then checking them for
        validity.
        """

        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid() and self.object.status != 2:
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        Called if all forms are valid. Updates a moderation and then redirects to a
        success page.
        """
        self.object = form.save(commit=False)
        self.object.end_moderate = timezone.now()
        self.object = form.save()
        """
        If Ad is approved changed Advertisement's field 'is_visible' to True.
        """
        if self.object.status == 1:
            self.activate_visible_ad()
        return super(ModerationFinishedView, self).form_valid(form)

    def activate_visible_ad(self):
        ad = get_object_or_404(self.model2, pk=self.object.ad_to_moderate.id)
        ad.is_visible = True
        ad.save()
        return True


class ModerationDetailView(LoginModeratorRequiredMixin, DetailView):
    model = Moderation
    template_name = 'detail_moderation.html'
