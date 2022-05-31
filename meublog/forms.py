from django import forms
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _

from meublog.models import Comentario


class EmailPost(forms.Form):
    nome = forms.CharField(max_length=50)
    email = forms.EmailField()
    para = forms.EmailField()
    coments = forms.CharField(required=False,
                              widget=forms.Textarea)

    def enviar_email(self, meupost):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        para = self.cleaned_data['para']
        coments = self.cleaned_data['coments']

        conteudo = _('Leia o post') + ':' + meupost.titulo +\
                   _('Comentários') + ':' + coments
        mail = EmailMessage(
            subject=f"{nome} {_('recomenda ler o Post')} {meupost.titulo}",
            body=f'{conteudo}',
            from_email='contato@meublog.com.br',
            to=['contato@meublog.com.br', ],
            headers={'Reply-To': email}
        )
        mail.send()


class ComentarioModelForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['nome', 'email', 'corpo']

    def inserirComentario(self, post):
        #post_id = post.id
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        corpo = self.cleaned_data['corpo']

        novo_coment = self.save(commit=False)
        novo_coment.post = post
        novo_coment.save()

