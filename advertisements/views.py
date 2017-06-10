from django.shortcuts import render, get_object_or_404, HttpResponseRedirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, mail_admins



from advertisements.forms import AdvertisementForm, AdvertisementMessageForm
from advertisements.models import Advertisement, AdvertisementMessage

from utils import gen_page_list


def advertisements(request):
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
    # print("проверка", advertisement)
    form = AdvertisementMessageForm()
    # send_email('тема письма', 'само тело письма.', 'd.protsiuk@gmail.com',
    #           ['procent83@ukr.net'])
    if request.method == "POST":
        form = AdvertisementMessageForm(request.POST)
        if form.is_valid():
            print('тема письма будет', advertisement.title)
            """test send email"""
            email_visitor = form.cleaned_data['email_visitor']
            title = advertisement.title#("title")
            text = form.cleaned_data['text']
            email_author = advertisement.author.email

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
            send_mail("Subject BIG", "Data sent: %s %s" % (title, text),
                      email_visitor,
                      [email_author],
                      fail_silently=False)
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



