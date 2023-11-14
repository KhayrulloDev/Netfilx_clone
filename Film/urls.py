from django.urls import path
from .views import ActorAPIView, MovieAPIView


urlpatterns = [
    path('actor', ActorAPIView.as_view(), name='actor'),
    path('movie', MovieAPIView.as_view(), name='movie'),
]