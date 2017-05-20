from django.shortcuts import render

def advertisements(request):
    form = PublicationForm()
    if request.method == "POST":
        form = PublicationForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            Publication.objects.create(title=data.get("title"),
                                       body=data.get("body"),
                                       image=data.get("image"),
                                       author=request.user)
    publications = Publication.objects.all()