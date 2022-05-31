from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import translation
from django.utils.translation import gettext as _

from .models import Post, Comentario
from .forms import EmailPost, ComentarioModelForm
from django.views.generic import ListView, DetailView, FormView, CreateView, DeleteView, UpdateView, TemplateView


class ListarPostsView(ListView):
    queryset = Post.publicados.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'meublog/post/listarposts.html'

    def get_context_data(self, **kwargs):
        context = super(ListarPostsView, self).get_context_data(**kwargs)
        idioma = translation.get_language()
        context['idioma'] = idioma
        return context


class DetalharPostView(DetailView):
    template_name = 'meublog/post/detalharpost.html'
    model = Post

    def get_coments(self, id_post):
        try:
            return Comentario.objects.filter(post_id=id_post)
        except Comentario.DoesNotExist:
            raise Exception

    def get_context_data(self, **kwargs):
        context = super(DetalharPostView, self).get_context_data(**kwargs)
        idioma = translation.get_language()
        context['idioma'] = idioma
        context['coments'] = self.get_coments(self.object.id)
        return context


class FormContatoView(FormView):
    template_name = 'meublog/post/share.html'
    form_class = EmailPost
    success_url = reverse_lazy('meublog:listar_posts')
    meupost = Post()

    def get_post(self, id_post):
        try:
            return Post.publicados.get(pk=id_post)
        except Post.DoesNotExist:
            raise Exception

    def get_context_data(self, **kwargs):
        context = super(FormContatoView, self).get_context_data(**kwargs)
        idioma = translation.get_language()
        context['idioma'] = idioma
        context['post'] = self.get_post(self.kwargs['pk'])
        return context

    def form_valid(self, form, *args, **kwargs):
        meupost = self.get_context_data()['post']
        form.enviar_email(meupost)
        messages.success(self.request, _('Post') + ' ' +
                         meupost.titulo + ' ' + _('enviado com sucesso'))
        return super(FormContatoView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        meupost = self.get_context_data()['post']
        messages.error(self.request, _('Erro ao enviar o post') +
                       ' ' + meupost)
        return super(FormContatoView, self).form_invalid(form, *args, **kwargs)


class CriarComentarioView(CreateView):
    template_name = 'meublog/post/comentarios.html'
    model = Comentario
    form_class = ComentarioModelForm
    success_url = reverse_lazy('meublog:detalhar_post')

    def get_post(self, id_post):
        try:
            post = Post.publicados.get(pk=id_post)
            return post
        except Post.DoesNotExist:
            raise Exception

    def get_context_data(self, **kwargs):
        context = super(CriarComentarioView, self).get_context_data(**kwargs)
        idioma = translation.get_language()
        context['idioma'] = idioma
        context['post'] = self.get_post(self.kwargs['pk'])
        return context

    def form_valid(self, form, *args, **kwargs):
        post = self.get_post(self.kwargs['pk'])
        form.inserirComentario(post)
        # return super(CriarComentarioView, self).form_valid(form, *args, **kwargs)
        return redirect('meublog:detalhar_post', post.slug)

    def form_invalid(self, form, *args, **kwargs):
        return super(CriarComentarioView, self).form_invalid(form, *args, **kwargs)


class CadUsuarioView(SuccessMessageMixin, CreateView):
    template_name = 'meublog/usuarios/cadastro.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('meublog:loginuser')

    def get_context_data(self, **kwargs):
        context = super(CadUsuarioView, self).get_context_data(**kwargs)
        idioma = translation.get_language()
        context['idioma'] = idioma
        return context

    def form_valid(self, form, *args, **kwargs):
        # usuario = form.save(commit=False)
        # grupo = Group.objects.get(name='clientes_blog')
        # ERRO aqui
        # usuario.groups.add(grupo) # preciso pegar id de usuário antes de vincular a um grupo
        form.cleaned_data
        form.save()
        messages.success(self.request, _('Usuário cadastrado com sucesso'))
        return super(CadUsuarioView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, _("Usuário não pode ser cadastrado"))
        return super(CadUsuarioView, self).form_invalid(form, *args, **kwargs)


class LoginUsuarioView(FormView):
    template_name = 'meublog/usuarios/login.html'
    model = User
    form_class = AuthenticationForm
    success_url = reverse_lazy('meublog:listar_posts')

    def get_context_data(self, **kwargs):
        context = super(LoginUsuarioView, self).get_context_data(**kwargs)
        idioma = translation.get_language()
        context['idioma'] = idioma
        return context

    def form_valid(self, form, *args, **kwargs):
        nome = form.cleaned_data['username']
        senha = form.cleaned_data['password']
        usuario = authenticate(self.request, username=nome, password=senha)
        if usuario is not None:
            login(self.request, usuario)
            return redirect('meublog:listar_posts')
        messages.success(self.request, _('Bem vindo') + ' ' + usuario.username)
        return redirect('meublog:loginuser')

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, _("Usuário não pode fazer login"))
        return redirect('meublog:listar_posts')


class LogoutView(LoginRequiredMixin, LogoutView):
    def get(self, request):
        logout(request)
        # return HttpResponseRedirect(reverse('meublog:loginuser'))
        return redirect('meublog:listar_posts')
