from django.core.mail import send_mail, mail_admins, send_mass_mail
from django.db import models
from django.template.loader import render_to_string


class Documento(models.Model):
    num_doc = models.CharField(max_length=50)

    def __str__(self):
        return self.num_doc


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    salary = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    bio = models.TextField(default='N/A')
    photo = models.ImageField(upload_to='clients_photos', null=True, blank=True)
    doc = models.OneToOneField(Documento, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('deletar_cliente', 'Deletar Cliente'),
        )

    @property
    def nome_completo(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.first_name


    def save(self, *args, **kwargs):
        super(Person, self).save(*args, **kwargs)

        dados = {'cliente': self.nome_completo }
        texto_puro = render_to_string('clientes/emails/novo_cliente.txt', dados)
        email_html = render_to_string('clientes/emails/novo_cliente.html', dados)

        send_mail(
            'Novo cliente cadastrado',
            texto_puro,
            'postmaster@sandbox1d93f7aa880d44889b72578267c4477c.mailgun.org',
            ['severos1982@gmail.com'],
            html_message=email_html,
            fail_silently=False,
        )

        # E-mails enviandos pelos admins cadastrados em settings.py
        # Normalmente utilizado em try { } em funções essenciais no sistema
        # caso ocorra algo que não era esperado.
        #mail_admins(
        #    'Novo cliente cadastrado',
        #    texto_puro,
        #    html_message=email_html,
        #    fail_silently=False,
        #)

        # Envio de emails em massa
        #message1 = ('Subject here', 'Here is the message', 'from@example.com', ['first@example.com', 'other@example.com'])
        #message2 = ('Another Subject', 'Here is another message', 'from@example.com', ['second@test.com'])
        #send_mass_mail((message1, message2), fail_silently=False)