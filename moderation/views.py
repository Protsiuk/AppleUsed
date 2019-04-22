from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, HttpResponseRedirect
from moderation.models import Moderation
from moderation.forms import ModerationForm
from advertisements.models import Advertisement
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View, ListView, UpdateView, DetailView


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
    template_name = 'list_for_moderation.html'
    paginate_by = 15

    # def get(self, request, *args, **qwargs):
    #     context = self.get_context_data()
    #     return self.render_to_response(context)

    def get_queryset(self, **kwargs):
        # ad_at_work = self.model.objects.filter(status=2)
        # ad_rejected = self.model.objects.filter(status=0)
        qs = Advertisement.objects.filter(is_visible=False, is_moderated=False)
        # # qs = list_ad
        # # qs = [list_ad.exclude(pk=ad.ad_to_moderate_id) for ad in ad_at_work if list_ad.filter(pk=ad.ad_to_moderate_id).exists()]
        #
        # for ad in ad_at_work:
        #     pk = ad.ad_to_moderate_id
        #     if qs.filter(pk=pk).exists():
        #         qs = qs.exclude(pk=pk)

        return qs


class MyListModerationView(LoginModeratorRequiredMixin, ListView):
    """
    Return a list Ads, which request user are moderated.
    """
    model = Moderation
    template_name = 'my_list_moderation.html'
    paginate_by = 15

    def get_queryset(self, **kwargs):
        qs = self.model.objects.filter(moderator=self.request.user).order_by('-end_moderate')
        return qs


class ModerationBeginView(LoginModeratorRequiredMixin, View):
    model = Moderation
    model2 = Advertisement

    """Create object of moderation"""

    def get(self, request, *args, **kwargs):
        self.object = Moderation()
        user = self.request.user
        self.object.moderator = user
        pk = self.kwargs['pk']
        self.object.ad_to_moderate = get_object_or_404(self.model2, pk=pk)
        self.object.status = 2
        self.object.save()
        """
        Changed Advertisement's field 'is_moderated' to True.
        """
        self.is_moderated_ad()
        return redirect(self.get_absolute_url(pk=self.object.moderation_id))

    def get_absolute_url(self, pk):
        return reverse('moderation:moderate_ad', args=(pk,))

    def is_moderated_ad(self):
        ad = get_object_or_404(self.model2, pk=self.object.ad_to_moderate.id)
        ad.is_moderated = True
        # ad.updated = ad.updated
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
        # print('FINISHEd CHECKING')
        return super(ModerationFinishedView, self).form_valid(form)

    def activate_visible_ad(self):
        ad = get_object_or_404(self.model2, pk=self.object.ad_to_moderate.id)
        ad.is_visible = True
        # ad.updated = ad.updated
        ad.save()
        return True


class ModerationDetailView(LoginModeratorRequiredMixin, DetailView):
    model = Moderation
    template_name = 'detail_moderation.html'

    # def get_context_data(self, **kwargs):
    #     context = super(ModerationDetailView, self).get_context_data(**kwargs)
    #     return context


