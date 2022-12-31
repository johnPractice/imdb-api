from rest_framework import serializers
from djangoProject1.apps.imdb_vod.models import IMDBModel, GalleryModel, RelatedContentModel
from djangoProject1.apps.utils.http_exceptions import ItemExistHttpException


class InputIMDBContentSerializer(serializers.Serializer):
    imdb_code = serializers.CharField(max_length=12,
                                      allow_blank=False)

    def validate_imdb_code(self, value):
        if IMDBModel.check_content_exist_with_imdb_id(imdb_id=value):
            raise ItemExistHttpException()
        return value


class CreatorIMDBContentSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):

        db_instant = super().save(**kwargs)
        GalleryModel.create_gallery_for_content_with_list_image(
            image_list=self.context['galleries'], imdb_content=db_instant)
        return db_instant

    class Meta:
        model = IMDBModel
        fields = '__all__'


class IMDBContentGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryModel
        fields = ('image_url',)


class IMDBSingleConetentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IMDBModel
        fields = ("id", "imdb_id", "title",
                  "rate", "main_poster", "description")


class IMDBRelatedConetentSerializer(serializers.ModelSerializer):
    data = IMDBSingleConetentSerializer(source='imdb_related_content')

    class Meta:
        model = RelatedContentModel
        fields = ("data",)


class IMDBContentRetrieveSerializer(serializers.ModelSerializer):
    gallery = IMDBContentGallerySerializer(
        many=True, source='imdb_content_gallery')
    related = IMDBRelatedConetentSerializer(
        many=True, source='content_origin_related')

    class Meta:
        model = IMDBModel
        fields = ("id", "imdb_id", "title", "gallery", "related",
                  "rate", "main_poster", "description")
