from django.urls import path
from . import views

app_name = 'meublog'

urlpatterns = [
    #path('', views.listar_posts, name='listar_posts'),
    path('', views.ListarPostsView.as_view(), name='listar_posts'),
    path('<slug:slug>/',
         views.DetalharPostView.as_view(),
         name='detalhar_post'),
    path('share/<int:pk>/',
         views.FormContatoView.as_view(),
         name='post_share'),
    path('comentar/<int:pk>', views.CriarComentarioView.as_view(),
         name='comentar_post'),
    path('cadastrarusuario', views.CadUsuarioView.as_view(), name='cadastrouser'),
    path('logar', views.LoginUsuarioView.as_view(), name='loginuser'),
    path('logout', views.LogoutView.as_view(), name='logoutuser'),
]
