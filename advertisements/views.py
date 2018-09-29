from django.shortcuts import render, get_object_or_404, HttpResponseRedirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from advertisements.forms import AdvertisementForm, AdvertisementMessageForm, AdvertisementFilterForm
from advertisements.models import Advertisement, AdvertisementMessage

from utils import gen_page_list


"""def advertisements(request):
    form = AdvertisementForm()
    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            AdvertisementMessage.objects.create(title=data.get("title"),
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
"""


                # return render(request, "advertisements.html", {"advertisements": advertisements,
                #                                                "form": form,
                #                                                "page_nums": page_nums})
            # data = form.cleaned_data['min_price']
            # AdvertisementMessage.objects.create(title=data.get("title"),
            #                              body=data.get("body"),
            #                              image=data.get("image"),
            #                              price=data.get("price"),
            #                              type_equipment=data.get("type_equipment"),
            #                              author=request.user)



def advertisements(request):
    # print ('ZAPROS'+request.GET)
    # form = AdvertisementFilterForm()
    form_filter = AdvertisementFilterForm(request.GET)

    # form = AdvertisementForm()
    advertisements = Advertisement.objects.all()
    if request.GET.get("serch"):
        find = request.GET.get("serch")
        # advertisements = find_advertisements(request, advertisements)
        advertisements = advertisements.filter(title__icontains=find)


    if form_filter.is_valid():
        # if form_filter.cleaned_data["find"]:
        #     print(True)
        #     find = request.GET.get("find")
        #     # advertisements = find_advertisements(request, advertisements)
        #     advertisements = advertisements.filter(title__icontains=find)
        if form_filter.cleaned_data['min_price']:
            advertisements = advertisements.filter(price__gte=form_filter.cleaned_data['min_price'])

        if form_filter.cleaned_data['max_price']:
            advertisements = advertisements.filter(price__lte=form_filter.cleaned_data['max_price'])

        if form_filter.cleaned_data['ordering']:
            advertisements = advertisements.order_by(form_filter.cleaned_data['ordering'])
        # advertisements = filter_list(request, form_filter, advertisements)

    # if request.GET.get("find"):
    #     advertisements = find_title(request, advertisements)
    # advertisements = advertisements.order_by("-added")

    # advertisements = Advertisement.objects.order_by("-added")
    # pagination of pages
    paginator = Paginator(advertisements, 5)
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
                                                 "form_filter": form_filter,
                                                 "page_nums": page_nums,
                                                   'len_advertisments': len(advertisements)})


#---------------------------
def filter_list(request, form_filter, advertisements):
    print(request.GET, "it was REQUEST")
    if form_filter.cleaned_data["min_price"]:
        advertisements = advertisements.filter(price__gte=form_filter.cleaned_data['min_price'])

    if form_filter.cleaned_data["max_price"]:
        advertisements = advertisements.filter(price__lte=form_filter.cleaned_data['max_price'])

    if form_filter.cleaned_data["ordering"]:
        advertisements = advertisements.order_by(form_filter.cleaned_data["ordering"])

    return (advertisements)
#----------------------------------

    # return {"advertisements": advertisements, "form_filter": form_filter}

# def ordering_list(request, form_filter, advertisements):
#     advertisements = advertisements.order_by(form_filter.cleaned_data["ordering"])
#     return (advertisements)


# def ordering_list(request, advertisements):
#     # print('request самые дешевые')
#     advertisements = Advertisement.objects.all()
#     form_filter = AdvertisementFilterForm(request.GET)
#     if request.GET.get("GET/advertisements/order_price_inexpensive/"):
#         print('самые дешевые')
#         advertisements = Advertisement.objects.order_by("-price")
#         return render(request, "advertisements_sorted_inexpensive.html", {"advertisements": advertisements,
#                                                                         "form_filter": form_filter})
#     elif request.GET.get("/advertisements/order_price_expensive/"):
#         advertisements = Advertisement.objects.order_by("price")
#         return render(request, "advertisements_sorted_expensive.html", {"advertisements": advertisements})




    # advertisements = advertisements.order_by(form_filter.cleaned_data["ordering"])
    # return (advertisements)


def serch_advertisements(request, advertisements):
    find = request.GET.get("find")

    # print(request.GET)
    advertisements = advertisements.filter(title__icontains=find)
    return (advertisements)


# def ordering_list(request, advertisements):
#     ordering = request.GET.get("ordering")
#     advertisements = Advertisement.objects.order_by(ordering)
#
#     return (advertisements)
#----------------------------------------------------------------

#     if request.method == "POST":
#         form = AdvertisementForm(request.POST, request.FILES)
#         if form.is_valid():
#             data = form.cleaned_data
#             Advertisement.objects.create(title=data.get("title"),
#                                          body=data.get("body"),
#                                          image=data.get("image"),
#                                          price=data.get("price"),
#                                          type_equipment=data.get("type_equipment"),
#                                          author=request.user)

""" #views.py
def some_view(request):
    ....
    if 'sort_by' in request.GET:
        sort_by = request.GET['sort_by']
    else:
        sort_by = None
    ....

#template.html
<a href="?page={{ content.next_page_number }}{% if sort_by %}&sort_by={{ sort_by }}{% endif %}">Следующая страница</a>
"""
    # advertisements = Advertisement.objects.order_by("-added")



    # # pagination of pages
    # paginator = Paginator(advertisements, 5)
    # page = request.GET.get('page', 1)
    # # print(paginator.num_pages, "pages number")
    # try:
    #     advertisements = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     advertisements = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     advertisements = paginator.page(paginator.num_pages)
    # page_nums = gen_page_list(int(page), paginator.num_pages)
    #
    # return render(request, "advertisements.html", {"advertisements": advertisements,
    #                                              "form": form,
    #                                              "page_nums": page_nums})

@login_required(login_url="/accounts/login/")
def create_advertisement(request):
    form = AdvertisementForm()
    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            data = form.cleaned_data
            # data = form
            Advertisement.objects.create(title=data.get("title"),
                                         body=data.get("body"),
                                         image=data.get("image"),
                                         price=data.get("price"),
                                         type_equipment=data.get("type_equipment"),
                                         author=request.user,
                                         phone_author=data.get("phone_author"))
            advertisements = Advertisement.objects.all()
            return render(request, 'send_advertisement_success.html')
    return render(request, 'create_advertisement.html', {'form': form})
    # return HttpResponseRedirect(reverse("advertisements"))


def single_advertisement(request, advertisement_id):
    advertisement = get_object_or_404(Advertisement, pk=advertisement_id)
    # print("проверка", advertisement)
    form = AdvertisementMessageForm()
    # send_email('тема письма', 'само тело письма.', 'd.protsiuk@gmail.com',
    #           ['procent83@ukr.net'])
    if request.method == "POST":
        form = AdvertisementMessageForm(request.POST)
        if form.is_valid():
            print('тема письма будет', advertisement.title)
            """test send email"""
            # email_visitor = form.cleaned_data['email_visitor']
            # title = advertisement.title#("title")
            # text = form.cleaned_data['text']
            # email_author = advertisement.author.email

            # server = smtplib.SMTP("smtp.gmail.com 587)
            # server.ehlo()
            # server.starttls()
            # server.login("myGmailAccount", "o_MyPassword")
            # message = "\r\n".join([ \
            #     "From: {}".format(email_from), \
            #     "To: {}".format(email_to), \
            #     "Subject: {}".format(subject), \
            #     "", \
            #     "{}".format(text) \
            #     ])
            # server.sendmail("myYandexAccount@ya.ru", email_to, message)
            # server.quit()


            # Advertisement.objects.create(advertisement=advertisement,
            #                                   # author=user.email,
            #                                   email_visitor=form.cleaned_data['email_visitor'],
            #                                   # message=form.cleaned_data['text'],
            #                                   text=form.cleaned_data['text'])
            """
            send_mail("Subject BIG", "Data sent: %s %s" % (title, text),
                      email_visitor,
                      [email_author],
                      fail_silently=True)
            """
            return HttpResponseRedirect(reverse("single_advertisement", kwargs={"advertisement_id": advertisement_id}))
    # print("проверка", advertisement)
    # msg = EmailMessage(
    #     subject=u'Тема письма',
    #     body=u'тело сообщения тут',
    #     from_email= form.email_visitor,
    #     to=(request.user.email,),
    #     headers={'From': 'email_from@me.com'}
    # )
    # msg.content_subtype = 'html'
    # msg.send()
    return render(request, "single_advertisement.html", {"advertisement": advertisement,
                                                       "form": form})


def advertisements_expensive(request):
    # print ('ZAPROS'+request.GET)
    form = AdvertisementFilterForm()
    form_filter = AdvertisementFilterForm(request.GET)

    # form = AdvertisementForm()
    advertisements = Advertisement.objects.all()

    advertisements = advertisements.order_by("-price")

    # pagination of pages
    paginator = Paginator(advertisements, 10)
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

    return render(request, "advertisements_sorted_inexpensive.html", {"advertisements": advertisements,
                                                   "form_filter": form_filter,
                                                   "page_nums": page_nums})

    # GET /advertisements/order_price_inexpensive