import json
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from djangoProject1.apps.imdb_vod.models import IMDBModel

client = APIClient()


class TestCRUDIMDBCrud(TestCase):
    def setUp(self):
        __added_content = IMDBModel(imdb_id='tt9051908', description='test', rate=0.0, )
        __added_content.save()
        self.content_data = __added_content

    def test_create_new_content(self):
        res = client.post('/api/imdb/', data=json.dumps({"imdb_code": "tt14208870"}), content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_add_duplicate_imdb_id(self):
        res = client.post('/api/imdb/', data=json.dumps({"imdb_code": "tt9051908"}), content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT)

    def test_get_content_with_id(self):
        res = client.get('/api/imdb/'+self.content_data.id.__str__())
        self.assertEqual(status.HTTP_200_OK, res.status_code)

    def test_get_list_content(self):
        res = client.get('/api/imdb/')
        self.assertEqual(status.HTTP_200_OK, res.status_code)
