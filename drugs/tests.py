import json

from django.contrib.auth.models import User
from django.test import TestCase, Client

from django.urls import reverse
from rest_framework import status

from drugs.models import Drug


class DrugSetUp(TestCase):
    def setUp(self):
        self.client = Client()
        self.content_type = 'application/json'

        self.user_username = "user_test"
        self.user_email = "user_test@test.cl"
        self.user_password = "top_secret"
        self.user = User.objects.create(username=self.user_username, email=self.user_email)
        self.user.set_password(self.user_password)
        self.user.save()

        login_data = json.dumps({'username': self.user_username, 'password': self.user_password})
        resp = self.client.post(reverse('token_obtain_pair'), login_data, content_type=self.content_type)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in resp.data)
        self.token = resp.data.get('access', None)

        token_data = json.dumps({'token': self.token})
        resp = self.client.post(reverse('token_verify'), token_data, content_type=self.content_type)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}

        self.drug = Drug.objects.create(name='Drug1', code='drug1', description='drug1')


class TestDrugListCreateView(DrugSetUp):

    def test_get(self):
        resp = self.client.get(reverse('drug:list_create'), content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        drug_list = resp.data

        drug_count = Drug.objects.count()
        self.assertEqual(len(drug_list), drug_count)

    def test_post(self):
        drug_count = Drug.objects.count()

        new_drug_data = {
            'name': 'Drug 2',
            'code': 'drug2',
            'description': 'Drug 2 description'
        }

        resp = self.client.post(reverse('drug:list_create'), new_drug_data, content_type=self.content_type,
                                **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        drug_count += 1
        self.assertEqual(drug_count, Drug.objects.count())

        drug_count = Drug.objects.count()
        new_drug_data = {
            'name': 'Drug 3',
            'code': 'drug2',
            'description': 'Drug 3 description'
        }
        resp = self.client.post(reverse('drug:list_create'), new_drug_data, content_type=self.content_type,
                                **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue('code' in resp.data)
        self.assertEqual(drug_count, Drug.objects.count())


class TestDrugRetrieveUpdateDestroyView(DrugSetUp):

    def test_get(self):
        resp = self.client.get(reverse('drug:retrieve_update_delete', kwargs={'id': self.drug.id}),
                               content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        drug_data = resp.data

        self.assertEqual(drug_data['code'], self.drug.code)

        resp = self.client.get(reverse('drug:retrieve_update_delete', kwargs={'id': 1000}),
                               **self.headers, content_type=self.content_type)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch(self):
        new_code = 'drug1patch'
        new_drug_data = {
            'code': new_code,
        }
        resp = self.client.patch(reverse('drug:retrieve_update_delete', kwargs={'id': self.drug.id}), new_drug_data,
                                 content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        current_drug = Drug.objects.first()
        self.assertEqual(current_drug.code, new_code)

        new_code = 'drug1patchdrug1patch'
        new_drug_data = {
            'code': new_code,
        }
        resp = self.client.patch(reverse('drug:retrieve_update_delete', kwargs={'id': self.drug.id}), new_drug_data,
                                 content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('code' in resp.data)

        resp = self.client.patch(reverse('drug:retrieve_update_delete', kwargs={'id': 1000}), new_drug_data,
                                 content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_put(self):
        new_code = 'drug1put'
        drug_update_data = {
            'name': self.drug.name,
            'code': new_code,
            'description': self.drug.description
        }
        resp = self.client.put(reverse('drug:retrieve_update_delete', kwargs={'id': self.drug.id}), drug_update_data,
                               content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        current_drug = Drug.objects.first()
        self.assertEqual(current_drug.code, new_code)

        new_code = 'drug1putdrug1put'
        drug_update_data = {
            'name': self.drug.name,
            'code': new_code,
            'description': self.drug.description
        }
        resp = self.client.patch(reverse('drug:retrieve_update_delete', kwargs={'id': self.drug.id}), drug_update_data,
                                 content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('code' in resp.data)

        resp = self.client.put(reverse('drug:retrieve_update_delete', kwargs={'id': 1000}), drug_update_data,
                               content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete(self):
        drug_count = Drug.objects.count()

        resp = self.client.delete(reverse('drug:retrieve_update_delete', kwargs={'id': self.drug.id}),
                                  content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        drug_count -= 1

        self.assertEqual(drug_count, Drug.objects.count())

        resp = self.client.delete(reverse('drug:retrieve_update_delete', kwargs={'id': 1000}),
                                  content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(drug_count, Drug.objects.count())
