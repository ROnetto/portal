import json
import random
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase, Client

from django.urls import reverse
from rest_framework import status

from drugs.models import Drug
from vaccinations.models import Vaccination


class VaccinationSetUp(TestCase):
    def setUp(self):
        self.client = Client()
        self.content_type = 'application/json'

        self.user_username = "user_test"
        self.user_email = "user_test@test.cl"
        self.user_password = "top_secret"
        self.user = User.objects.create(username=self.user_username, email=self.user_email)
        self.user.set_password(self.user_password)
        self.user.save()

        self.valid_rut = '115417479'
        self.invalid_rut = '11541747k'

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
        self.vaccination = Vaccination.objects.create(rut=self.valid_rut, dose='0.15', drug=self.drug)


class TestVaccinationListCreateView(VaccinationSetUp):

    def test_get(self):
        resp = self.client.get(reverse('vaccination:list_create'), content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        vaccination_list = resp.data

        vaccination_count = Vaccination.objects.count()
        self.assertEqual(len(vaccination_list), vaccination_count)

    def test_post(self):
        vaccination_count = Vaccination.objects.count()

        new_vaccination_data = {
            'rut': self.valid_rut,
            'dose': Decimal(random.randrange(15, 100)) / 100,
            'drug_id': self.drug.id
        }

        resp = self.client.post(reverse('vaccination:list_create'), new_vaccination_data,
                                content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        self.assertEqual(vaccination_count + 1, Vaccination.objects.count())

        vaccination_count = Vaccination.objects.count()
        new_vaccination_data = {
            'rut': self.invalid_rut,
            'dose': Decimal(random.randrange(15, 100)) / 100,
            'drug_id': self.drug.id
        }
        resp = self.client.post(reverse('vaccination:list_create'), new_vaccination_data,
                                content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue('rut' in resp.data)
        self.assertEqual(vaccination_count, Vaccination.objects.count())


class TestVaccinationRetrieveUpdateDestroyView(VaccinationSetUp):

    def test_get(self):
        resp = self.client.get(reverse('vaccination:retrieve_update_delete', kwargs={'id': self.vaccination.id}),
                               content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        vaccination_data = resp.data

        self.assertEqual(vaccination_data['rut'], self.vaccination.rut)

        resp = self.client.get(reverse('vaccination:retrieve_update_delete', kwargs={'id': 1000}),
                               content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch(self):
        new_dose = Decimal(random.randrange(15, 100)) / 100
        new_vaccination_data = {
            'dose': new_dose,
        }
        resp = self.client.patch(reverse('vaccination:retrieve_update_delete', kwargs={'id': self.vaccination.id}),
                                 new_vaccination_data, content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        current_vaccination = Vaccination.objects.first()
        self.assertEqual(current_vaccination.dose, new_dose)

        new_dose = Decimal(random.randrange(110, 150)) / 100
        new_vaccination_data = {
            'dose': new_dose,
        }
        resp = self.client.patch(reverse('vaccination:retrieve_update_delete', kwargs={'id': self.vaccination.id}),
                                 new_vaccination_data, content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('dose' in resp.data)

        resp = self.client.patch(reverse('vaccination:retrieve_update_delete', kwargs={'id': 1000}),
                                 new_vaccination_data, content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_put(self):
        new_dose = Decimal(random.randrange(15, 100)) / 100
        vaccination_update_data = {
            'rut': self.vaccination.rut,
            'dose': new_dose,
            'drug_id': self.vaccination.drug.id
        }
        resp = self.client.put(reverse('vaccination:retrieve_update_delete', kwargs={'id': self.vaccination.id}),
                               vaccination_update_data, content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        current_vaccination = Vaccination.objects.first()
        self.assertEqual(current_vaccination.dose, new_dose)

        new_dose = Decimal(random.randrange(110, 150)) / 100
        vaccination_update_data = {
            'rut': self.vaccination.rut,
            'dose': new_dose,
            'drug_id': self.vaccination.drug.id
        }
        resp = self.client.put(reverse('vaccination:retrieve_update_delete', kwargs={'id': self.vaccination.id}),
                               vaccination_update_data, content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('dose' in resp.data)

        resp = self.client.put(reverse('vaccination:retrieve_update_delete', kwargs={'id': 1000}),
                               vaccination_update_data, content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete(self):
        vaccination_count = Vaccination.objects.count()

        resp = self.client.delete(reverse('vaccination:retrieve_update_delete', kwargs={'id': self.vaccination.id}),
                                  content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        vaccination_count -= 1

        self.assertEqual(vaccination_count, Vaccination.objects.count())

        resp = self.client.delete(reverse('vaccination:retrieve_update_delete', kwargs={'id': 1000}),
                                  content_type=self.content_type, **self.headers)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(vaccination_count, Vaccination.objects.count())
