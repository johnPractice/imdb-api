from django.contrib import admin
from djangoProject1.apps.imdb_vod.models import IMDBModel, GalleryModel, RelatedContentModel


class IMDBRelatedAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class IMDBAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')


admin.site.register(IMDBModel, IMDBAdmin)
admin.site.register(GalleryModel, GalleryAdmin)
admin.site.register(RelatedContentModel, IMDBRelatedAdmin)
