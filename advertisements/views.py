from django.shortcuts import render, get_object_or_404, HttpResponseRedirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse


from advertisements.forms import AdvertisementForm, AdvertisementMessageForm
from advertisements.models import Advertisement

from utils import gen_page_list


def advertisements(request):
    form = AdvertisementForm()
    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            Advertisement.objects.create(title=data.get("title"),
                                         body=data.get("body"),
                                         image=data.get("image"),
                                         price=data.get("price"),
                                         type_equipment=data.get("type_equipment"),
                                         author=request.user)
    advertisements = Advertisement.objects.order_by("-added")

    # pagination of pages
    paginator = Paginator(advertisements, 1)
    page = request.GET.get('page', 1)
    # print(paginator.num_pages, "pages number")
    try:
        advertisements = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        advertisements = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        advertisements = paginator.page(paginator.num_pages)
    page_nums = gen_page_list(int(page), paginator.num_pages)

    return render(request, "advertisements.html", {"advertisements": advertisements,
                                                 "form": form,
                                                 "page_nums": page_nums})




















def new_advertisement(request):
    form = AdvertisementForm()
    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            Advertisement.objects.create(title=data.get("title"),
                                         body=data.get("body"),
                                         image=data.get("image"),
                                         price=data.get("price"),
                                         type_equipment=data.get("type_equipment"),
                                         author=request.user)
    advertisements = Advertisement.objects.all()


def single_advertisement(request, advertisement_id):
    advertisement = get_object_or_404(Advertisement, pk=advertisement_id)
    form = AdvertisementMessageForm()
    if request.method == "POST":
        form = AdvertisementMessageForm(request.POST)
        if form.is_valid():
            AdvertisementForm.objects.create(advertisement=advertisement,
                                              user=request.user,
                                              text=form.cleaned_data['text'])
            return HttpResponseRedirect(reverse("single_advertisement", kwargs={"advertisement_id": advertisement_id}))
    return render(request, "single_advertisement.html", {"advertisement": advertisement,
                                                       "form": form})
