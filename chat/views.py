from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from chat.models import Message, Chat
from chat.forms import UserMessageForm


class DialogsListView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'dialog_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = self.model.objects.filter(Q(last_send_message__sender_msg=self.request.user)|
                                       Q(last_send_message__receiver_msg=self.request.user))
        return qs.order_by('-last_send_message__pub_date')


class CurrentDialogView(LoginRequiredMixin, FormMixin, DetailView):
    model = Chat
    model2 = Message
    template_name = 'dialog.html'
    form_class = UserMessageForm

    def get_success_url(self):
        return reverse('chat:current_dialog', kwargs={'pk': self.kwargs['pk']})

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and get current dialog. If hadn't redirected to dialog list User is not chats member.
        """
        self.object = self.get_object()
        if self.request.user == self.object.last_send_message.sender_msg or \
                        self.request.user == self.object.last_send_message.receiver_msg:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        else:
            return redirect('chat:dialog_list')

    def get_context_data(self, **kwargs):
        context = super(CurrentDialogView, self).get_context_data(**kwargs)
        self.get_or_set_readed()
        context['form_message'] = UserMessageForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_or_set_readed(self, **kwargs):
        current_viewer = self.request.user
        try:
            chat = get_object_or_404(self.model, id=self.kwargs['pk'])
            last_msg = Message.objects.filter(chat_id=chat.id).latest('pub_date')
            if not last_msg.is_readed and current_viewer == last_msg.receiver_msg:
                list_msg = Message.objects.filter(chat_id=chat.id).order_by('-pub_date')
                for msg in list_msg:
                    if not msg.is_readed and current_viewer == msg.receiver_msg:
                        msg.is_readed = True
                        msg.reading_date = timezone.now()
                        msg.save()
        except ObjectDoesNotExist:
            return reverse_lazy('chat:dialog_list')
        return None

    def form_valid(self, form):
        """
        Called if form is valid. Create a New message in current dialog and then redirects to a
        success page (current dialog).
        """
        new_message = form.save(commit=False)
        new_message.subject_ad = self.object.last_send_message.subject_ad
        new_message.chat = get_object_or_404(self.model, id=self.kwargs['pk'])
        new_message.sender_msg = self.request.user

        chat_id = new_message.chat.id
        last_msg = Message.objects.filter(chat_id=chat_id).latest('pub_date')
        if self.request.user != last_msg.receiver_msg:
            new_message.receiver_msg = last_msg.receiver_msg
        else:
            new_message.receiver_msg = last_msg.sender_msg
        new_message = form.save()
        chat = Chat.objects.get(pk=new_message.chat.id)
        chat.last_send_message = new_message
        chat.save()
        self.send_mail_to_receiver(receiver=last_msg.receiver_msg, subject=last_msg.subject_ad.title)
        # self.object = form.save()
        return super(CurrentDialogView, self).form_valid(form)

    def send_mail_to_receiver(self, receiver, subject):
        current_site = get_current_site(self.request)
        domen = current_site.domain
        subject_msg = 'Вы получили ответ на объявление '+subject
        receiver = receiver.email
        body = 'Вы получили новое сообщение по '+subject+'\n перейдите по адресу http://'+domen+self.get_success_url()
        email_message = EmailMessage(subject=subject_msg, body=body, to=[receiver])
        email_message.send()
        return 'ok'


class DeleteDialogView(LoginRequiredMixin, DeleteView):
    model = Chat
    success_url = reverse_lazy('chat:dialog_list')
    template_name = 'dialog_delete.html'

    def get_object(self, queryset=None):
        chat = get_object_or_404(Chat, pk=self.kwargs['pk'])
        return chat
