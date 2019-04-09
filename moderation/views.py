from django.shortcuts import render
from moderation.models import Moderation, Moderator
from advertisements.models import Advertisement
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
# from django.core.urlresolvers import reverse_lazy

from django.views.generic import View, CreateView, FormView, RedirectView, ListView, UpdateView, DetailView, DeleteView

# Create your views here.

# class PermForModerateMixin()


class ListForModerateView(LoginRequiredMixin, ListView):
    model = Moderation
    # success_url = '/advertisements/search-list/'
    template_name = 'list_for_moderation.html'
    paginate_by = 15

    def get_queryset(self):
        # qs = super(ListForModerateView, self).get_queryset()
        qs = Advertisement.objects.filter(is_visible=False)
        # qs = Moderation.objects.filter(ad_to_moderate__is_visible=False)
        # qs = self.model.objects.filter(ad_to_moderate__is_visible=True)#.order_by('-ad_to_moderate__created')
        # print(qs)
        return qs

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated or request.user.is_staff:
    #         return self.handle_no_permission()
    #     return super(ListForModerateView, self).dispatch(request, *args, **kwargs)

    # def handle_no_permission(self):
    #     if self.raise_exception:
    #         raise PermissionDenied(self.get_permission_denied_message())
    #     return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

