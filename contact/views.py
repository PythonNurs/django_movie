from .models import Contact
from .forms import ContactForm
from django.views.generic import CreateView
from .tasks import send_info_email


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        send_info_email.delay(form.instance.email)
        return super().form_valid(form)
