from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .views import MovieViewSet, ActorViewSet, MovieActorAPIView, CommentAPIView

router = DefaultRouter()
router.register('movies', MovieViewSet)
router.register('actors', ActorViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('movies/<int:id>/actors', MovieActorAPIView.as_view(), name='movie-actors'),
    path('auth/', views.obtain_auth_token),
    path('get-comments', CommentAPIView.as_view, name='get_comment')
]