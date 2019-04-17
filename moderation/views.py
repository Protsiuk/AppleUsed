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

# class PermForModerateMixin()


class ListForModerateView(LoginRequiredMixin, ListView):
    model = Moderation
    # success_url = '/advertisements/search-list/'
    template_name = 'list_for_moderation.html'
    paginate_by = 15

    def get_queryset(self, **kwargs):
        # qs = super(ListForModerateView, self).get_queryset()
        ad_at_work = self.model.objects.filter(status=3)
        qs = Advertisement.objects.filter(is_visible=False)
        # qs = list_ad
        # qs = [list_ad.exclude(pk=ad.ad_to_moderate_id) for ad in ad_at_work if list_ad.filter(pk=ad.ad_to_moderate_id).exists()]

        for ad in ad_at_work:
            pk = ad.ad_to_moderate_id
            if qs.filter(pk=pk).exists():
                qs = qs.exclude(pk=pk)
        # qs = Moderation.objects.filter(ad_to_moderate__is_visible=False, status=2)
        # qs = self.model.objects.filter(ad_to_moderate__is_visible=True)#.order_by('-ad_to_moderate__created')
        return qs

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated or request.user.is_staff:
    #         return self.handle_no_permission()
    #     return super(ListForModerateView, self).dispatch(request, *args, **kwargs)

    # def handle_no_permission(self):
    #     if self.raise_exception:
    #         raise PermissionDenied(self.get_permission_denied_message())
    #     return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

# class TestStartview(CreateView):
#     model = Moderation
#     form_class = ModerationForm
#     template_name = 'detail_moderation.html'
#     success_url = '/list_for_moderation/'


class ModerationBeginView(LoginRequiredMixin, View):
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
        self.object.status = 3
        # self.object.end_moderate = None
        self.object.save()
        print(pk)
        # return redirect('profile_user') # its worcked
        return reverse('moderate_detail')

        # return redirect(self.get_success_url(pk=self.object.moderation_id))


        # return redirect(self.get_absolute_url(pk=self.object.moderation_id))
        # return HttpResponseRedirect(self.get_success_url())

    def get_absolute_url(self, pk):
        print(pk)
        return 'moderation:moderate/%s/' % pk

    def get_success_url(self, pk):
        print(pk)
        # return 'moderation:moderate/%s/' % pk
        return HttpResponseRedirect(reverse('profile_user'))


class ModerationFinishedView(LoginRequiredMixin, UpdateView):
    model = Moderation
    success_url = '/moderation/'
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
        # self.instance = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if self.object.status == 3:
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
        print('POST IS - ', self.object)
        if form.is_valid():
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
        self.object.is_visible = True
        self.object = form.save()
        # self.object.is_visible = False
        print('FINISHEd CHECKING')
        return super(ModerationFinishedView, self).form_valid(form)




    # def form_invalid(self, form):
    #     """
    #     Called if a form is invalid. Re-renders the context data with the
    #     data-filled forms and errors.
    #     """
    #     return self.render_to_response(
    #         self.get_context_data(form=form))

        # return HttpResponseRedirect(reverse("moderate_detail", kwargs={"moderation_id": self.object.id}))
        # return HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self):
    #     return reverse_lazy('moderation')




    # def get_context_data(self, **kwargs):
    #
    #     """
    #     Insert the single object into the context dict.
    #     """
    #
    #     user = self.request.user
    #     pk_ad = self.kwargs['pk']
    #     print(pk_ad)
    #     ad = self.model2.objects.filter(pk=pk_ad)
    #     context = {}
    #     # self.object = None
    #     context['moderator'] = user
    #     context['ad_to_moderate'] = str(ad)
    #     # context['time_sending_by_user'] = ad.created
    #     # context['end_moderate'] = None
    #     context['status'] = 'at_work'
    #
    #     # if self.object:
    #     #     # context['object'] = self.object
    #     #     self.object = None
    #     #     self.object['moderator'] = user
    #     #     self.object['ad_to_moderate'] = ad
    #     #     self.object['time_sending_by_user'] = ''
    #     #     self.object['end_moderate'] = None
    #     #     self.object['status'] = 'at_work'
    #
    #     #     context_object_name = self.get_context_object_name(self.object)
    #     #     if context_object_name:
    #     #         context[context_object_name] = self.object
    #     # context.update(kwargs)
    #     print(context)
    #     return super(ModerationBeginView, self).get_context_data(**context)



        # ctx = super(ModerationBeginView, self).get_context_data(**kwargs)
        # # id = request.GET['ad-id']
        #
        # pk_ad = self.kwargs['pk']
        # ad = self.model2.objects.filter(pk=pk_ad)
        #
        # print(ad)
        # obj = self.model.objects.filter(ad_to_moderate=ad)
        # print(type(obj))
        # # ctx = get_object_or_404(Moderation, pk=1)
        #
        # # obj = get_object_or_404(Moderation, pk=self.object.ad_to_moderate__id)
        # # user = self.request.user
        #
        # # self.object = None
        # # self.object['moderator'] = user
        # # self.object['ad_to_moderate'] = obj
        # # self.object['time_sending_by_user'] = ''
        # # self.object['end_moderate'] = None
        # # self.object['status'] = 'at_work'
        # # return Response(self.object)
        #
        # # ctx = super(ModerationBeginView, self).get_context_data(**kwargs)
        # print(type(ctx))
        # return ctx



# class ModerationStartView(LoginRequiredMixin, CreateView):
#     model = Moderation
#     model2 = Advertisement
#     success_url = '/moderation/'
#     # form_class = AdvertisementForm
#     template_name = 'detail_moderation.html'
#
#     """Start moderation"""
#
#     def get(self, request, pk=None, format=None):
#         """
#         Return New object of Moderation.
#         """
#         id = request.GET['ad-id']
#         obj = get_object_or_404(Advertisement, pk=self.kwargs['pk'])
#         user = self.request.user
#         self.object = None
#         self.object['moderator'] = user
#         self.object['ad_to_moderate'] = obj
#         self.object['time_sending_by_user'] = ''
#         self.object['end_moderate'] = None
#         self.object['status'] = 'at_work'
#         return Response(self.object)
#
#     # def get(self, request, *args, **kwargs):
#     #     self.object = self.model2.objects.get(pk=kwargs['pk'])
#     #     # print('REQUEST - ', request)
#     #     return self.object
#
#         # return super(BaseCreateView, self).get(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         ctx = get_object_or_404(self.model2, pk=self.kwargs['pk'])
#         # ctx = self.model2.objects.get(pk=id)
#         ctx['moderator'] = self.request.user
#         print('REQUEST - ', ctx)
#         return ctx
#
#     # def get(self, request, *args, **kwargs):
#     #     """
#     #     Handles GET requests and instantiates blank versions of the form
#     #     and.
#     #     """
#     #     # self.object = None
#     #     print('REQUEST - ', request)
#     #     obj = self.model2.objects.get(pk=self.kwargs['pk'])
#     #     return self.render_to_response(obj)
#
#
#         # return self.render_to_response(
#         #     self.get_context_data(form=form,
#         #                           image_form=image_form))
#
#
# # def get_context_data(self, **kwargs):
# #     context = super(AdvertisementCreateView, self).get_context_data(**kwargs)
# #     if self.request.POST:
# #         context['advertisementimage_form'] = AdvertisementImageFormSet(self.request.POST)
# #     else:
# #         context['advertisementimage_form'] = AdvertisementImageFormSet()
# #     return context


# class ModerationCreateView(LoginRequiredMixin, CreateView):
#     model = Advertisement
#     success_url = '/moderation/'
#     # form_class = AdvertisementForm
#     # template_name = 'create_advertisement.html'
#     """Create NEW moderation"""
#     # fields = ['username', 'first_name', 'last_name', 'birth_day', 'email', 'location_user', 'phone_number_user']
#     # print()
#
#     # def get(self, request, *args, **kwargs):
#     #     """
#     #     Handles GET requests and instantiates blank versions of the form
#     #     and its inline formsets.
#     #     """
#     #     self.object = None
#     #     form_class = self.get_form_class()
#     #     form = self.get_form(form_class)
#     #     image_form = AdvertisementImageFormSet()
#     #     return self.render_to_response(
#     #         self.get_context_data(form=form,
#     #                               image_form=image_form))
#     #
#     # def post(self, request, *args, **kwargs):
#     #     """
#     #     Handles POST requests, instantiating a form instance and its inline
#     #     formsets with the passed POST variables and then checking them for
#     #     validity.
#     #     """
#     #     self.object = None
#     #     form_class = self.get_form_class()
#     #     form = self.get_form(form_class)
#     #     image_form = AdvertisementImageFormSet(request.POST, request.FILES)#, queryset=AdvertisementImage.objects.none())
#     #     # image_form = AdvertisementImageForm(self.request.POST or None, self.request.FILES or None)
#     #     # print(request.POST)
#     #     if (form.is_valid() and image_form.is_valid()):
#     #         return self.form_valid(form, image_form)
#     #     else:
#     #         return self.form_invalid(form, image_form)
#     #
#     # def form_valid(self, form, image_form):
#     #     """
#     #     Called if all forms are valid. Creates a Advertisement instance along with
#     #     associated AdvertisementImage (ImageFormsets Images) and then redirects to a
#     #     success page.
#     #     """
#     #     form.instance.author = self.request.user
#     #     self.object = form.save()
#     #     image_form.instance = self.object
#     #     image_form.save()
#     #     return HttpResponseRedirect(self.get_success_url())
#     #
#     # def form_invalid(self, form, image_form):
#     #     """
#     #     Called if a form is invalid. Re-renders the context data with the
#     #     data-filled forms and errors.
#     #     """
#     #     return self.render_to_response(
#     #         self.get_context_data(form=form,
#     #                               image_form=image_form))
#     #
#     # def get_context_data(self, **kwargs):
#     #     context = super(AdvertisementCreateView, self).get_context_data(**kwargs)
#     #     if self.request.POST:
#     #         context['advertisementimage_form'] = AdvertisementImageFormSet(self.request.POST)
#     #     else:
#     #         context['advertisementimage_form'] = AdvertisementImageFormSet()
#     #     return context
#
# class AjaxAPIModerationStartView(APIView):
#     model = Moderation
#     model2 = Advertisement
#     success_url = '/moderation/'
#     # form_class = AdvertisementForm
#     template_name = 'detail_moderation.html'
#
#     """Start moderation"""
#
#     authentication_classes = (authentication.SessionAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)
#
#     # def post(self, request, pk=None, format=None):
#     #     pass
#
#
#     def get(self, request, pk=None, format=None):
#         """
#         Return New object of Moderation .
#         """
#         obj = get_object_or_404(Advertisement, pk=self.kwargs['pk'])
#         user = self.request.user
#         self.object = None
#         self.object['moderator'] = user
#         self.object['ad_to_moderate'] = obj
#         self.object['time_sending_by_user'] = ''
#         self.object['end_moderate'] = None
#         self.object['status'] = 'at_work'
#         return Response(self.object)
#
#
#         # obj = get_object_or_404(Advertisement, pk=self.kwargs['pk'])
#         # user = self.request.user
#         # admark, created = AdvertisementFollowing.objects.get_or_create(user=user,
#         #                                                                advertisement_id=self.kwargs['pk'])
#         # url_ = admark.get_api_absolute_url()
#         # url_ = admark.get_absolute_url()
#         # if not created:
#         #     admark.delete()
#         #     data = {
#         #         'ad_mark': False,
#         #         'url_favorite_icon': '/static/img/favorite_FALSE.png'
#         #     }
#         # else:
#         #     data = {
#         #         'ad_mark': True,
#         #         'url_favorite_icon': '/static/img/favorite_TRUE.png'
#         #     }
#         #
#         # return Response(data)
#
#
# class ModerationBeginView2(LoginRequiredMixin, DetailView):
#     model = Moderation
#     model2 = Advertisement
#     success_url = '/moderation/'
#     # form_class = AdvertisementForm
#     template_name = 'detail2_moderation.html'
#
#     """Start moderation"""
#
#
#     # def get(self, request, *args, **kwargs):
#
#     def get_context_data(self, **kwargs):
#         """
#         Return New object of Moderation.
#         """
#         ctx = super(ModerationBeginView2, self).get_context_data(**kwargs)
#         # id = request.GET['ad-id']
#
#         pk_ad = self.kwargs['pk']
#         ad = self.model2.objects.filter(pk=pk_ad)
#
#         print(ad)
#         obj = self.model.objects.filter(ad_to_moderate=ad)
#         print(type(obj))
#         # ctx = get_object_or_404(Moderation, pk=1)
#
#         # obj = get_object_or_404(Moderation, pk=self.object.ad_to_moderate__id)
#         # user = self.request.user
#
#         # self.object = None
#         # self.object['moderator'] = user
#         # self.object['ad_to_moderate'] = obj
#         # self.object['time_sending_by_user'] = ''
#         # self.object['end_moderate'] = None
#         # self.object['status'] = 'at_work'
#         # return Response(self.object)
#
#         # ctx = super(ModerationBeginView, self).get_context_data(**kwargs)
#         print(type(ctx))
#         return ctx
#
#     # def get(self, request, pk=None, format=None):
#     #     """
#     #     Return New object of Moderation.
#     #     """
#     #     id = request.GET['ad-id']
#     #     obj = get_object_or_404(Advertisement, pk=self.kwargs['pk'])
#     #     user = self.request.user
#     #     self.object = None
#     #     self.object['moderator'] = user
#     #     self.object['ad_to_moderate'] = obj
#     #     self.object['time_sending_by_user'] = ''
#     #     self.object['end_moderate'] = None
#     #     self.object['status'] = 'at_work'
#     #     return Response(self.object)

