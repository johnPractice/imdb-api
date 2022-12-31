from rest_framework import status
from rest_framework import viewsets, generics

from rest_framework.response import Response
from djangoProject1.apps.imdb_vod.serializers import InputIMDBContentSerializer, IMDBContentRetrieveSerializer, \
    CreatorIMDBContentSerializer
from djangoProject1.apps.imdb_vod.utils.imdb_scraper import IMDb
from djangoProject1.apps.imdb_vod.models import IMDBModel
from djangoProject1.apps.utils.messages import ToastMessages
from djangoProject1.apps.imdb_vod.utils.imdb_creator import prepare_imdb_model_data
from rest_framework.decorators import action


class IMDBViewSet(generics.GenericAPIView, viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        imdb_content = IMDBModel.get_by_id_or_none(pk)
        if imdb_content is None:
            # TODO: its better create HTTPException multi type and handel it with appropriate exception
            return Response(data={"message": ToastMessages.USER_iTEM_NOT_FOUND.value}, status=status.HTTP_404_NOT_FOUND)
        serializer = IMDBContentRetrieveSerializer(imdb_content)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

    def create(self, request):
        input_data_serializer = InputIMDBContentSerializer(data=request.data)
        input_data_serializer.is_valid(raise_exception=True)
        imdb_id = input_data_serializer.data["imdb_code"]
        if IMDBModel.check_content_exist_with_imdb_id(imdb_id):  # can handel it here or serializer
            return Response(data={"message": ToastMessages.ITEM_EXISTS.value}, status=status.HTTP_409_CONFLICT)
        imdb_data = IMDb().getAllFeatures(imdb_id)
        new_imdb_content = CreatorIMDBContentSerializer(data=prepare_imdb_model_data(imdb_data))
        new_imdb_content.is_valid(raise_exception=True)
        new_imdb_content.save()
        return Response(data=new_imdb_content.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        search_input = request.query_params.get('search', '')
        search_type = request.query_params.get('type', 'all')
        queryset = IMDBModel.search_with_imdb_id_or_title(search_input=search_input, search_type=search_type)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = IMDBContentRetrieveSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = IMDBContentRetrieveSerializer(queryset, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    # @action(detail=True, url_path='add-related/')
    # def add_related_content(self, request, pk=None):
    #     imdb_content = IMDBModel.get_by_id_or_none(pk)
    #     if imdb_content is None:
    #         return Response(data={"message": ToastMessages.USER_iTEM_NOT_FOUND.value}, status=status.HTTP_404_NOT_FOUND)
    #
