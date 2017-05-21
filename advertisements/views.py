from django.shortcuts import render
from advertisements.forms import AdvertisementForm
from advertisements.models import Advertisement


def advertisements(request):
    form = AdvertisementForm()
    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            Advertisement.objects.create(title=data.get("title"),
                                         body=data.get("body"),
                                         image=data.get("image"),
                                         type_equipment=data.get("type_equipment"),
                                         author=request.user)
    advertisements = Advertisement.objects.all()

def single_advertisement(request, advertisement_id):
    advertisement = get_object_or_404(Advertisement, pk=advertisement_id)
    # form = PublicationCommentForm()
    if request.method == "POST":
        form = PublicationCommentForm(request.POST)
        if form.is_valid():
            PublicationComment.objects.create(advertisement=advertisement,
                                              user=request.user,
                                              text=form.cleaned_data['text'])
            return HttpResponseRedirect(reverse("single_publication", kwargs={"publication_id": advertisement_id}))
    return render(request, "single_advertisement.html", {"publication": advertisement,
                                                       "form": form})
    # publication = Publication.objects.get(pk=publication_id)


# def advertisement(request):
#     form = AdvertisementForm()
#     if request.method == "POST":
#         form = AdvertisementForm(request.POST, request.FILES)
#         if form.is_valid():
#             data = form.cleaned_data
#             Advertisement.objects.create(title=data.get("title"),
#                                        body=data.get("body"),
#                                        image=data.get("image"),
#                                        author=request.user)
#     advertisements = Advertisement.objects.all()


# new_advertisement