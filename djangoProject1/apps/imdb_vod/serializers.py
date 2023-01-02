from threading import Thread
import logging
from rest_framework import serializers
from djangoProject1.apps.imdb_vod.models import IMDBModel, GalleryModel, RelatedContentModel
from djangoProject1.apps.utils.http_exceptions import ItemExistHttpException
from djangoProject1.apps.imdb_vod.utils.imdb_scraper import IMDb
from djangoProject1.apps.imdb_vod.utils.imdb_creator import prepare_imdb_model_data


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
        if self.context.get('check_set_related', True):
            related_thread = Thread(
                target=self.__create_related_content, args=(self.context.get('related_id', []), db_instant))
            related_thread.start()
            # related_thread.join() ## if want run sync uncomment this line
        return db_instant

    def __create_related_content(self, related_content_list_id: list[str], content_instance: IMDBModel) -> None:
        for imdb_id in related_content_list_id:
            try:
                imdb_raw_data = IMDb().getAllFeatures(imdb_id=imdb_id)
                new_imdb_content = CreatorIMDBContentSerializer(
                    data=prepare_imdb_model_data(imdb_raw_data), context={"check_set_related": False, "galleries": IMDb().getGalleriesImage(imdb_id)})
                new_imdb_content.is_valid(raise_exception=True)
                new_imdb_content = new_imdb_content.save()
                RelatedContentModel(imdb_origin_content=content_instance,
                                    imdb_related_content=new_imdb_content).save()
            except Exception as e:
                logging.error(e)

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
