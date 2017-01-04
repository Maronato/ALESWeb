from django import forms
from django.core.mail import send_mail
from django.conf import settings


class ContactForm(forms.Form):

    name = forms.CharField(label='Seu nome', max_length=30)
    email = forms.EmailField(label='Seu email')
    subject = forms.CharField(label='Assunto', max_length=30)
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}), label='Mensagem')

    def send(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        text = self.cleaned_data['text']

        send_mail(
            subject,
            name + ', ' + email + ', usou o site do ALES para contato:\n\n---------\n' + text + '\n---------\n\nLove,\nALES Bot.',
            email,
            settings.DEFAULT_CONTACT_EMAIL
        )
