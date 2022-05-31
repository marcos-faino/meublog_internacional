from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class PublicadosManager(models.Manager):
    def get_queryset(self):
        return super(PublicadosManager,
                     self).get_queryset().filter(status='publicado')


class Post(models.Model):
    STATUS_CHOICES = (
        ('rascunho', _('Rascunho')),
        ('publicado', _('Publicado'))
    )

    objects = models.Manager()
    publicados = PublicadosManager()

    titulo = models.CharField(max_length=250)
    slug = models.SlugField(max_length=100)
    corpo = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meublog_posts')
    publicado = models.DateTimeField(default=timezone.now)
    criado = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='rascunho')

    class Meta:
        ordering = ('-publicado',)
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    nome = models.CharField(_('Nome'), max_length=50)
    email = models.EmailField(_('E-mail'))
    corpo = models.TextField(_('Mensagem'))
    criado = models.DateTimeField(_('Data de criação'), auto_now_add=True)
    modificado = models.DateField(_('Data da atualização'), auto_now=True)
    ativo = models.BooleanField(_('Ativo'), default=True)

    class Meta:
        ordering = ('-criado',)

    def __str__(self):
        return _('Comentário de') + ': ' + self.nome
