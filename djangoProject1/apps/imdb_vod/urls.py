from django.urls import path
from rest_framework.routers import DefaultRouter
from djangoProject1.apps.imdb_vod.api.imdb_crud import IMDBViewSet

imdb_router = DefaultRouter()
imdb_router.register('', IMDBViewSet, basename='imdb urls')
urlpatterns = [
                  # add other urls
              ] + imdb_router.urls
