import json
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, get_list_or_404

from django.http import HttpResponse, Http404
from django.forms import formset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy
# from django.views import View

from django.views.generic import View, CreateView, FormView, RedirectView, ListView, UpdateView, DetailView, DeleteView

from advertisements.forms import AdvertisementForm, AdvertisementMessageForm,\
                                AdvertisementFilterForm, AdvertisementsSearchFilterMultiForm, AdvertisementImageForm,\
                                AdvertisementImageFormSet
from advertisements.models import Advertisement, AdvertisementMessage, AdvertisementFollowing, PageHit, AdvertisementImage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from accounts.models import MyCustomUser

from utils import gen_page_list


class AdvertisementHomeView(ListView):
    model = Advertisement
    success_url = '/advertisements/search-list/'
    template_name = 'main.html'

    def get_queryset(self):
        # qs = super(AdvertisementHomeView, self).get_queryset()
        qs = Advertisement.objects.order_by('-created').filter(is_active=True)[:4]
        return qs

    # def get_context_data(self, **kwargs):
    #     context = super(AdvertisementHomeView, self).get_context_data(**kwargs)
    #     advertisement = get_object_or_404(Advertisement, pk=self.kwargs['advertisement_id'])
    #     try:
    #         context['following'] = AdvertisementFollowing.objects.filter(user=self.request.user, advertisement=advertisement)
    #     except Exception:
    #         context['following'] = None
    #     return context

    # def get_queryset(self):
    #     queryset = []
    #     advertisements = Advertisement.objects.all().order_by('-created')
    #     # Get all images
    #     images = AdvertisementImage.objects.all()
    #     queryset.append(advertisements)
    #     queryset.append(images)
    #     print(queryset)
    #     return queryset


class AdvertisementsSearchView(ListView):
    model = Advertisement
    # success_url = '/advertisment/list/'
    template_name = 'search_list.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        # result = result.objects.filter(query)
        result = Advertisement.objects.search(query)
        from_min_price =self.request.GET.get('min_price')
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

    # def get_context_data(self, **kwargs):
    #     context = super(AdvertisementsSearchView, self).get_context_data(**kwargs)
    #     context['following'] = AdvertisementFollowing.objects.filter(user=self.request.user, is_following=True)
    #     return context


# class AdvertisementListMarksView(ListView):
#     model = AdvertisementFollowing
#     success_url = '/advertisements/favorites/'
#     template_name = 'main.html'
#     # queryset = AdvertisementImage.objects.filter(advertisementimage__image=True, advertisementimage__main_image=True)
#     # print(queryset.filter())
#
#     def get_queryset(self):
#         # qs = super(AdvertisementHomeView, self).get_queryset()
#         user = self.request.user
#         qs = AdvertisementFollowing.objects.filter(user=user)
#         # qs = Advertisement.objects.filter('-created').filter(is_active=True)[:4]
#         return qs

class MyAdvertisementActiveView(LoginRequiredMixin, ListView):
    model = Advertisement
    template_name = 'my_active_advertisements.html'

    def get_queryset(self):
        ctx = super(MyAdvertisementActiveView, self).get_queryset()
        author = self.request.user
        ctx = ctx.filter(author=author, is_active=True)
        return ctx


class MyAdvertisementArchiveView(LoginRequiredMixin, ListView):
    model = Advertisement
    template_name = 'archive_advertisements.html'

    def get_queryset(self):
        ctx = super(MyAdvertisementArchiveView, self).get_queryset()
        author = self.request.user
        ctx = ctx.filter(author=author, is_active=False)
        return ctx


# class MyAdvertisementView(LoginRequiredMixin, ListView):
#     model = Advertisement
#     template_name = 'my_advertisements.html'
#
#     def get_queryset(self):
#         ctx = super(MyAdvertisementView, self).get_queryset()
#         author = self.request.user
#         ctx = ctx.filter(author=author)
#         return ctx

#
# class AjaxAdvertisementMarkView(View):
#     template_name = 'advertisement_detail.html'
#     model = AdvertisementFollowing
#
#     def get(self, request, args, **kwargs):
#         ctx = []
#         if request.POST:
#             advertisement_id = self.request.GET.get('advertisement_id')
#             user_follower = request.user
#             # advertisementmark = self.model.objects
#             advertisementmark, created = self.model.objects.get_or_create(user=user_follower, obj_id=advertisement_id)
#             ctx['advertisementmark'] = advertisementmark
#             return render(request, self.template_name, ctx)


class AdvertisementsListMarksView(LoginRequiredMixin, ListView):
    model = Advertisement
    template_name = 'favorites.html'
    model_following = AdvertisementFollowing

    def get_queryset(self):
        qs = self.model.objects.filter(favorites__user=self.request.user)
        return qs


# class AdvertisementMarkMixinView(View):
#     model = AdvertisementFollowing
#     model_ad = Advertisement
#     template_name = 'advertisement_detail.html'
#
#     def get_object(self, queryset=None):
#         # ad = get_object_or_404()
#         advertisement = get_object_or_404(self.model_ad, pk=self.kwargs['pk'])
#         # user = self.request.user
#         return advertisement
#
#     def get(self, request, advertisement_id):
#         print('id ad is - ', advertisement_id)
#         user_follow = request.user
#         # пытаемся получить закладку из таблицы, или создать новую
#         advertisementmark, created = self.model.objects.get_or_create(user=user_follow, obj_id=advertisement_id)
#         # если не была создана новая закладка,
#         # то считаем, что запрос был на удаление закладки
#         # print(advertisementmark)
#         if not created:
#             advertisementmark.delete()
#         return advertisementmark


class AdvertisementMessageView(CreateView):
    model = AdvertisementMessage
    form_class = AdvertisementMessageForm
    template_name = 'advertisement_detail.html'


class AdvertisementCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    success_url = '/advertisements/'
    form_class = AdvertisementForm
    template_name = 'create_advertisement.html'
    """Create NEW advertisement"""
    # fields = ['username', 'first_name', 'last_name', 'birth_day', 'email', 'location_user', 'phone_number_user']

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
        # self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_form = AdvertisementImageFormSet(request.POST, request.FILES)#, queryset=AdvertisementImage.objects.none())
        # image_form = AdvertisementImageForm(self.request.POST or None, self.request.FILES or None)
        # print(request.POST)
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


class AdvertisementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Advertisement
    success_url = '/advertisements/my_active_advertisements/'
    form_class = AdvertisementForm
    template_name = 'update_advertisement.html'
    permission_denied_message = 'You can not edit this ad.'
    """Update existing advertisement"""

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    # def dispatch(self, request, *args, **kwargs):
    #     user_test_result = self.get_test_func()()
    #     if not request.user.is_authenticated:
    #         return self.handle_no_permission()
    #     else:
    #         if not user_test_result:
    #             return self.get_permission_denied_message()
    #     return super(AdvertisementUpdateView, self).dispatch(request, *args, **kwargs)

    # def dispatch(self, request, *args, **kwargs):
    #     obj = self.get_object()
    #     if obj.author != self.request.user:
    #         return Http404("You are not allowed to edit this Ad")
    #     return super(AdvertisementUpdateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # form.instance.author = self.request.user
        image_form = AdvertisementImageFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  image_form=image_form))

        # if self.object.author != self.request.user:
        #     print('ne author')
        #     return self.render_to_response(self.get_permission_denied_message())
        #     # return self.handle_no_permission()
        #     # return (self.get_permission_denied_message())
        # else:
        #     form_class = self.get_form_class()
        #     form = self.get_form(form_class)
        #     # form.instance.author = self.request.user
        #     image_form = AdvertisementImageFormSet()
        #     return self.render_to_response(
        #         self.get_context_data(form=form,
        #                               image_form=image_form))

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
        print(self.object)
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
        # form.instance.author = self.request.user
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


class AjaxAdmarkView(RedirectView):
    # в данную переменную будет устанавливаться модель закладок, которую необходимо обработать
    # model = None
    model = AdvertisementFollowing

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Advertisement, pk=self.kwargs['pk'])
        # obj = get_object_or_404(Advertisement, pk=self.kwargs['pk'])
        user = self.request.user
        admark, created = self.model.objects.get_or_create(user=user, obj_id=ad.id)
        if not created:
            admark.delete()
        url_ = admark.get_absolute_url()
        return url_


class AjaxAPIAdmarkView(APIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None, format=None):
        """
        Return True if hadn't a relation .
        """
        # obj = get_object_or_404(Advertisement, pk=self.kwargs['pk'])
        user = self.request.user
        admark, created = AdvertisementFollowing.objects.get_or_create(user=user, advertisement_id=self.kwargs['pk'])
        # url_ = admark.get_api_absolute_url()
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


class AdvertisementDetailView(DetailView):
    model = Advertisement
    model_hits = PageHit
    model_following = AdvertisementFollowing
    template_name = 'advertisement_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AdvertisementDetailView, self).get_context_data(**kwargs)
        advertisement = get_object_or_404(Advertisement, pk=self.kwargs['pk'])
        user = self.request.user
        context['img_following'] = self.following(user, advertisement)
        views_page = self.hit_count(user, advertisement)
        context['views_page'] = views_page
        if user == advertisement.author:
            context['you_is_author'] = True
        return context

    """
    Counter for views pages
    If user is not author counter increment +1
    """
    def hit_count(self, user, advertisement):

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

    """
    Add or remove page to favorites list
    Create relate current user to current ad if hasn't before, or remove if it had.
    """

    def following(self, user, advertisement):
        try:
            follow = AdvertisementFollowing.objects.get(user=user, advertisement=advertisement)
            following = '/static/img/favorite_TRUE.png'
        except AdvertisementFollowing.DoesNotExist:
            following = '/static/img/favorite_FALSE.png'
        return following

        # # нам потребуется пользователь
        # print("user_follow is ", user)
        # # пытаемся получить закладку из таблицы, или создать новую
        # # bookmark, created = self.model.objects.get_or_create(user=user, obj_id=pk)
        # following, created = self.model_following.objects.get_or_create(user=user, advertisement=advertisement)
        # # если не была создана новая закладка,
        # # то считаем, что запрос был на удаление закладки
        # if not created:
        #     following.delete()
        # # return HttpResponseRedirect(reverse_lazy('advertisement_detail'))
        # return following


class AdvertisementDeleteView(DeleteView):
    model = Advertisement
    success_url = reverse_lazy('main')
    template_name = 'advertisement_delete.html'

    def get_object(self, queryset=None):
        advertisement = get_object_or_404(Advertisement, pk=self.kwargs['pk'])
        return advertisement

    def get_success_url(self):
        return reverse_lazy('search_list')
