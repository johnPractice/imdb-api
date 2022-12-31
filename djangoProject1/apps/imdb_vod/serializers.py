from rest_framework import serializers
from djangoProject1.apps.imdb_vod.models import IMDBModel, GalleryModel, RelatedContentModel


class InputIMDBContentSerializer(serializers.Serializer):
    imdb_code = serializers.CharField(max_length=12,
                                      allow_blank=False)


class CreatorIMDBContentSerializer(serializers.ModelSerializer):
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
    gallery = IMDBContentGallerySerializer(many=True, source='imdb_content_gallery')
    related = IMDBRelatedConetentSerializer(many=True, source='content_origin_related')

    class Meta:
        model = IMDBModel
        fields = ("id", "imdb_id", "title", "gallery", "related",
                  "rate", "main_poster", "description")
