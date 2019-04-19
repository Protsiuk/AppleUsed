from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, HttpResponseRedirect
from moderation.models import Moderation
from moderation.forms import ModerationForm
from advertisements.models import Advertisement
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy


from django.views.generic import View, CreateView, FormView, RedirectView, ListView, UpdateView, DetailView, DeleteView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

# Create your views here.


class LoginModeratorRequiredMixin(LoginRequiredMixin):
    """
    Abstract CBV mixin that gives access mixins the same customizable
    functionality.
    """
    """
    CBV mixin which verifies that the current user is moderator or superuser authenticated.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_moderator:
            return self.handle_no_permission()
        return super(LoginModeratorRequiredMixin, self).dispatch(request, *args, **kwargs)


class ListForModerateView(LoginModeratorRequiredMixin, ListView):
    model = Moderation
    # success_url = '/advertisements/search-list/'
    template_name = 'list_for_moderation.html'
    paginate_by = 15

    def get_queryset(self, **kwargs):
        ad_at_work = self.model.objects.filter(status=3)
        qs = Advertisement.objects.filter(is_visible=False)
        # qs = list_ad
        # qs = [list_ad.exclude(pk=ad.ad_to_moderate_id) for ad in ad_at_work if list_ad.filter(pk=ad.ad_to_moderate_id).exists()]

        for ad in ad_at_work:
            pk = ad.ad_to_moderate_id
            if qs.filter(pk=pk).exists():
                qs = qs.exclude(pk=pk)
        # qs = self.model.objects.filter(ad_to_moderate__is_visible=True)#.order_by('-ad_to_moderate__created')
        return qs


class MyListModerationView(LoginModeratorRequiredMixin, ListView):
    model = Moderation
    # success_url = '/advertisements/search-list/'
    template_name = 'my_list_moderation.html'
    paginate_by = 15

    def get_queryset(self, **kwargs):
        # ad_of = self.model.objects.filter(moderator=self.request.user)
        qs = self.model.objects.filter(moderator=self.request.user)
        return qs


class ModerationBeginView(LoginModeratorRequiredMixin, View):
    model = Moderation
    model2 = Advertisement
    # success_url = '/moderate_detail/'
    # template_name = 'detail2_moderation.html'

    """Create object of moderation"""

    def get(self, request, *args, **kwargs):
        self.object = Moderation()
        user = self.request.user
        self.object.moderator = user
        pk = self.kwargs['pk']
        self.object.ad_to_moderate = get_object_or_404(self.model2, pk=pk)
        self.object.status = 2
        self.object.save()
        return redirect(self.get_absolute_url(pk=self.object.moderation_id))

    def get_absolute_url(self, pk):
        print(pk)
        return reverse('moderation:moderate_detail', args=(pk,))


class ModerationFinishedView(LoginModeratorRequiredMixin, UpdateView):
    model = Moderation
    model2 = Advertisement
    success_url = reverse_lazy('moderation:list_for_moderation')
    form_class = ModerationForm
    template_name = 'detail2_moderation.html'

    """
    Get created object of moderation
    and checking of Ad and dispatch to view for all off users
    """

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if self.object.status == 2:
            # ad = get_object_or_404(self.model2, pk=self.model.ad_to_moderate.id)
            # return super(ModerationFinishedView, self).get(request, *args, **kwargs)
            return self.render_to_response(
                self.get_context_data(form=form))
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

    # def get_context_data(self, **kwargs):
    #     context = super(ModerationFinishedView, self).get_context_data(**kwargs)
    #     # return super(ModerationFinishedView, self).get_context_data(**context)
    #     return context

    def form_valid(self, form):
        """
        Called if all forms are valid. Updates a Advertisement instance along with
        associated AdvertisementImage (ImageFormsets Images) and then redirects to a
        success page.
        """
        self.object = form.save(commit=False)
        self.object.end_moderate = timezone.now()
        # self.object.is_visible = True
        self.object = form.save()
        if self.object.status==1:
            self.activate_visible_ad()
        print('FINISHEd CHECKING')
        return super(ModerationFinishedView, self).form_valid(form)

    def activate_visible_ad(self):
        ad = get_object_or_404(self.model2, pk=self.object.ad_to_moderate.id)
        ad.is_visible = True
        ad.updated = ad.updated
        ad.save()
        return True


class ModerationDetailView(ListForModerateView, DetailView):
    model = Moderation
    template_name = 'detail_2_moderation.html'

    def get_context_data(self, **kwargs):
        context = super(ModerationDetailView, self).get_context_data(**kwargs)
        # context = get_object_or_404(self.model, pk=self.kwargs['pk'])
        # user = self.request.user
        print(context)
        return context



