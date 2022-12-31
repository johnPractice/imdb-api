from django.db import models
from djangoProject1.apps.utils.base_model import BaseModel
from django.db.models import Q


# maybe we need other provider
# for this scenario we need abstract model for "Content"
class IMDBModel(BaseModel):
    title = models.CharField(db_index=True
                             , max_length=300,
                             null=False,
                             blank=False, )
    description = models.TextField(blank=True)
    main_poster = models.URLField(null=True,
                                  blank=True)
    imdb_id = models.CharField(db_index=True,
                               unique=True,
                               max_length=12,
                               null=False,
                               blank=False)
    rate = models.FloatField(null=True,
                             blank=True,
                             default=0.0)

    @staticmethod
    def check_content_exist_with_imdb_id(imdb_id: str):
        try:
            IMDBModel.objects.get(imdb_id=imdb_id)
            return True
        except IMDBModel.DoesNotExist:
            return False

    @staticmethod
    def get_by_id_or_none(input_id):
        try:
            return IMDBModel.objects.prefetch_related('imdb_content_gallery', 'content_related').get(id=input_id)
        except IMDBModel.DoesNotExist:
            return None

    @staticmethod
    def search_with_imdb_id_or_title(search_input, search_type):
        imdb_id_query = Q(imdb_id__contains=search_input)
        title_query = Q(title__contains=search_input)
        query_type = {"title": title_query, 'imdb_id': imdb_id_query, 'both': imdb_id_query | title_query, 'all': Q()}
        if search_type not in query_type:
            search_type = 'all'

        return IMDBModel.objects.filter(query_type[search_type])


class GalleryModel(BaseModel):
    imdb_content = models.ForeignKey(IMDBModel,
                                     related_name='imdb_content_gallery',
                                     related_query_name='imdb_gallery',
                                     on_delete=models.CASCADE)
    image_url = models.URLField(null=False,
                                blank=False)  # if use postgres and use ARRAY(Charfield()) we can igonre this part and foreign key


class RelatedContentModel(BaseModel):
    imdb_origin_content = models.ForeignKey(IMDBModel,
                                            related_name='content_origin_related',
                                            related_query_name='content_origin_related',
                                            on_delete=models.CASCADE)
    imdb_related_content = models.ForeignKey(IMDBModel,
                                             related_name='content_related',
                                             related_query_name='content_related',
                                             on_delete=models.CASCADE)
