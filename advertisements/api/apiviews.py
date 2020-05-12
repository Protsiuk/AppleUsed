# from django.shortcuts import get_object_or_404, HttpResponseRedirect
#
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.exceptions import ObjectDoesNotExist
# from django.core.urlresolvers import reverse_lazy
# from django.core.mail import EmailMessage
#
# from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView, View
# from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib.sites.shortcuts import get_current_site
# from django.views.generic.edit import FormMixin
# from django.utils import timezone
# from django.urls import reverse

from django.http import Http404
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication

from advertisements.api.serializers import (
    AdvertisementSerializer,
    AdsListSerializer,
    SingleAdsSerializer,
    ImagesAssociatedAdvertisementSerializer,
    AdvertisementCreateSerializer,
    AdvertisementCreateUpdateSerializer,
    FavoriteAdvertisementSerializer
)
from advertisements.models import Advertisement, AdvertisementImage, AdvertisementFollowing


# from advertisements.forms import AdvertisementCreationForm, AdvertisementImageFormSet
# from advertisements.models import Advertisement, AdvertisementFollowing, PageHit
# from chat.forms import UserMessageForm, GuestMessageForm
# from chat.models import Message, Chat


class IsOwnerPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    message = "Yuo must be author of tht advertisement."

    def has_object_permission(self, request, view, obj=None):
        # Write permissions are only allowed to the owner of the snippet
        # return obj is None or obj.author == request.user
        return obj.author == request.user


# class IsOwnerPermission(BasePermission):
#     """
#     A base class from which separate permission classes should inherit.
#     """
#     def has_object_permission(self, request, view, obj):
#         try:
#             return request.user.is_superuser or getattr(obj, view.user_lookup_kwarg) == request.user
#         except:
#             pass
#         return request.user.is_superuser


class AdsListAPIView(ListAPIView):
    # """
    # get:
    # Get list of advertisements
    # """
    model = Advertisement
    serializer_class = AdsListSerializer
    # queryset = model.objects.filter(is_visible=True, is_active=True)

    # def get(self, request):
    #     advertisements = self.model.objects.filter(is_visible=True, is_active=True)
    #     # serializer = AdsListSerializer(advertisements, many=True)
    #     serializer = AdsListSerializer(advertisements, many=True)
    #     return Response({"advertisements": serializer.data})

    """
    get:
    Get search list of advertisements
    """

    def get_queryset(self):
        # print('1')
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


# class AdDetailAPIView(RetrieveAPIView):
#     model = Advertisement
#     # queryset = Advertisement.objects.all()
#     queryset = Advertisement.objects.filter(pk='pk')
#     serializer_class = AdvertisementSerializer


class AdDetailAPIView(APIView):
    model = Advertisement
    # queryset = Advertisement.objects.filter(pk='pk')
    serializer_class = SingleAdsSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Advertisement.objects.get(pk=pk)
        except Advertisement.DoesNotExist:
            raise Http404

    """
    GET:
    Get single advertisement.
    """
    # @APIView(['PUT', 'DELETE'])
    def get(self, request, pk):
        advertisement = self.get_object(pk)
        serializer = SingleAdsSerializer(advertisement)
        return Response(serializer.data)

    """
    POST:
    Create single advertisement.
    """
    def post(self, request, format=None):
        serializer = SingleAdsSerializer(data=request.data, fieles=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    """
    PUT:
    Update single advertisement.
    """
    def put(self, request, pk):
        advertisement = get_object_or_404(Advertisement.objects.all(), pk=pk)
        user = self.request.user
        # advertisement = self.get_object(pk)
        serializer = SingleAdsSerializer(advertisement, data=request.data)
        if serializer.is_valid() and self.request.user.is_authenticated:
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    DELETE:
    Delete current advertisement.
    """
    def delete(self, request, pk, format=None):
        advertisement = self.get_object(pk)
        advertisement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def get_object(self, advertisement_id):
    #     try:
    #         return Advertisement.objects.get(pk=advertisement_id)
    #     except Advertisement.DoesNotExist:
    #         raise Http404
    #
    # def get(self, request, advertisement_id):
    #     advertisement = self.get_object(advertisement_id)
    #     return Response(self.serializer_class(advertisement).data)
    #
    # def delete(self, request, advertisement_id):
    #     advertisement = self.get_object(advertisement_id)
    #     advertisement.delete()
    #     return Response({"success": True})





class AdDetailUpdateDeleteAPIView(APIView):
    model = Advertisement
    # queryset = Advertisement.objects.all()
    # queryset = Advertisement.objects.filter(pk='pk')
    serializer_class = SingleAdsSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Advertisement.objects.get(pk=pk)
        except Advertisement.DoesNotExist:
            raise Http404

    """
    GET:
    Get single advertisement.
    """
    # @APIView(['PUT', 'DELETE'])
    def get(self, request, pk):
        advertisement = self.get_object(pk)
        serializer = SingleAdsSerializer(advertisement)
        return Response(serializer.data)

    """
    POST:
    Create single advertisement.
    """
    def post(self, request, format=None):
        serializer = SingleAdsSerializer(data=request.data, fieles=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    """
    PUT:
    Update single advertisement.
    """
    def put(self, request, pk):
        advertisement = get_object_or_404(Advertisement.objects.all(), pk=pk)
        user = self.request.user
        # advertisement = self.get_object(pk)
        print(advertisement.description)
        serializer = SingleAdsSerializer(advertisement, data=request.data)
        if serializer.is_valid() and self.request.user.is_authenticated:
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    DELETE:
    Delete current advertisement.
    """
    def delete(self, request, pk, format=None):
        advertisement = self.get_object(pk)
        advertisement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def get_object(self, advertisement_id):
    #     try:
    #         return Advertisement.objects.get(pk=advertisement_id)
    #     except Advertisement.DoesNotExist:
    #         raise Http404
    #
    # def get(self, request, advertisement_id):
    #     advertisement = self.get_object(advertisement_id)
    #     return Response(self.serializer_class(advertisement).data)
    #
    # def delete(self, request, advertisement_id):
    #     advertisement = self.get_object(advertisement_id)
    #     advertisement.delete()
    #     return Response({"success": True})




class AdApiViewset(ModelViewSet):
    serializer_class = SingleAdsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Advertisement.objects.all()

    """Added author to Ads"""

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)


# class TestProjectViewSet(ModelViewSet):
#     queryset = Advertisement.objects.all().order_by('-created')
#     # serializer_class = SingleAdsSerializer
#     serializer_class = AdvertisementCreateSerializer

class TestProjectViewSet(CreateAPIView):
    # queryset = Advertisement.objects.all().order_by('-created')
    # serializer_class = SingleAdsSerializer
    model = Advertisement
    serializer_class = AdvertisementCreateSerializer

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)


class TestProjectPhotoViewSet(ModelViewSet):
    queryset = AdvertisementImage.objects.all().order_by('created')
    serializer_class = ImagesAssociatedAdvertisementSerializer


class TestUpload(ModelViewSet):
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all().order_by('-created')


    # print(queryset)
    # """Create NEW advertisement"""
    #
    # def get(self, request, *args, **kwargs):
    #     """
    #     Handles GET requests and instantiates blank versions of the form
    #     and its inline formsets.
    #     """
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     image_form = AdvertisementImageFormSet()
    #     return self.render_to_response(
    #         self.get_context_data(form=form,
    #                               image_form=image_form))
    #
    # def post(self, request, *args, **kwargs):
    #     """
    #     Handles POST requests, instantiating a form instance and its inline
    #     formsets with the passed POST variables and then checking them for
    #     validity.
    #     """
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     image_form = AdvertisementImageFormSet(request.POST,
    #                                            request.FILES)  # , queryset=AdvertisementImage.objects.none())
    #     if (form.is_valid() and image_form.is_valid()):
    #         return self.form_valid(form, image_form)
    #     else:
    #         return self.form_invalid(form, image_form)


class UpdateAdApiView(RetrieveUpdateAPIView):
    serializer_class = SingleAdsSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerPermission)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

# ---!!!---
class CreateAdApiView(CreateAPIView):
    serializer_class = AdvertisementCreateUpdateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Advertisement.objects.all()

    """Added author to Ads"""

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)


class AdRetrieveUpdateDeleteAPIView_2(APIView):
    # model = Advertisement
    # queryset = Advertisement.objects.all()
    # queryset = Advertisement.objects.filter(pk='pk')
    # serializer_class = AdvertisementCreateUpdateSerializer
    # serializer_class = SingleAdsSerializer

    def get_object(self, pk):
        try:
            return Advertisement.objects.get(pk=pk)
        except Advertisement.DoesNotExist:
            raise Http404

    """
    GET:
    Get single advertisement.
    """
    def get(self, request, pk):
        advertisement = self.get_object(pk)
        serializer = AdvertisementCreateUpdateSerializer(advertisement)
        return Response(serializer.data)

    """
    PUT:
    Update single advertisement.
    """

    def put(self, request, *args, **kwargs):
        advertisement_saved = self.get_object(pk=kwargs['pk'])
        print("pk is", advertisement_saved.pk)

        data = request.data.get('advertisement')
        serializer = AdvertisementCreateUpdateSerializer(instance=advertisement_saved, data=request.data, partial=True)
        if serializer.is_valid() and self.request.user.is_authenticated:
            advertisement_saved = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AdRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
class AdRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    model = Advertisement
    queryset = Advertisement.objects.all()
    # queryset = Advertisement.objects.filter(pk='pk')
    serializer_class = AdvertisementCreateUpdateSerializer
    # serializer_class = SingleAdsSerializer

    def get_object(self):
        try:
            return Advertisement.objects.get(pk=self.kwargs['pk'])
        except Advertisement.DoesNotExist:
            raise Http404
    #
    # """
    # GET:
    # Get single advertisement.
    # """
    # def get(self, request, pk):
    #     advertisement = self.get_object(pk)
    #     serializer = SingleAdsSerializer(advertisement)
    #     return Response(serializer.data)
    #
    """
    Update:
    Update single advertisement.
    """
    def update(self, request, *args, **kwargs):
        # Unify PATCH and PUT
        partial = True
        instance = self.get_object()

        # Create each PostImage
        for image in request.data.pop("images"):
            AdvertisementImage.objects.create(advertisement=instance, image=image)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # """
    # PUT:
    # Update single advertisement.
    # """
    # # def put(self, request, *args, **kwargs):
    # #     return self.update(request, *args, **kwargs)
    #
    # def put(self, request, *args, **kwargs):
    #     advertisement_saved = self.get_object()
    #     # advertisement_saved['images'] = AdvertisementImage.objects.filter(advertisement_id=advertisement_saved.id)
    #     print("pk is", advertisement_saved.images)
    #
    #     # data = request.data.get('advertisement')
    #     print(request.data.get('images_2'))
    #     serializer = AdvertisementCreateUpdateSerializer(instance=advertisement_saved, data=request.data, partial=True)
    #     if serializer.is_valid():# and self.request.user.is_authenticated:
    #         advertisement_saved = serializer.save()
    #         # print(serializer.data)
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # """
    # delete:
    # Delete single advertisement.
    # """
    # def delete(self, request, pk):
    #     advertisement = self.get_object(pk)
    #     advertisement.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# ---------


class AdvertisementsListMarksViewAPIView(ListAPIView):
    """
    Get list of favorites ads current user
    """
    model = AdvertisementFollowing
    serializer_class = FavoriteAdvertisementSerializer
    permission_classes = [permissions.IsAuthenticated]

    """
    get_queryset:
    Get list of favorites ads current user
    """

    def get_queryset(self):
        qs = self.model.objects.filter(user=self.request.user)#, is_visible=True)
        return qs


class MyAdvertisementActiveAPIView(ListAPIView, IsOwnerPermission):
    """
    Get a list of current user's ads
    """
    model = Advertisement
    serializer_class = AdsListSerializer

    """
    get_queryset:
    Get a list of current user's ads
    """

    def get_queryset(self):
        qs = self.model.objects.filter(author=self.request.user, is_active=True).order_by('-created')
        return qs


class MyAdvertisementArchiveAPIView(ListAPIView, IsOwnerPermission):
    """
    Get a list of current user's ads
    """
    model = Advertisement
    serializer_class = AdsListSerializer

    """
    get_queryset:
    Get a list of current user's ads
    """

    def get_queryset(self):
        qs = self.model.objects.filter(author=self.request.user, is_active=False).order_by('-created')
        return qs


class GetSinglePublicationView(APIView):
    serializer_class = AdvertisementSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, publication_id):
        try:
            return Advertisement.objects.get(pk=publication_id)
        except Advertisement.DoesNotExist:
            raise Http404

    def get(self, request, publication_id):
        publication = self.get_object(publication_id)
        return Response(self.serializer_class(publication).data)

    def delete(self, request, publication_id):
        publication = self.get_object(publication_id)
        publication.delete()
        return Response({"success": True})


class AdvDetailAPIViewSet(ModelViewSet):
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()
