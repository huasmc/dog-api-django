import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Puppy
from ..serializers import PuppySerializer

client = Client()

class GetAllPuppiesTest(TestCase):

    def setUp(self):
        Puppy.objects.create(
            name='Casper', age=3, breed='Bull Dog', color='Black')

        Puppy.objects.create(
            name='Muffin', age=1, breed='Gradane', color='Brown')

        Puppy.objects.create(
            name='Rambo', age=2, breed='Labrador', color='Black')

        Puppy.objects.create(
            name='Ricky', age=6, breed='Labrador', color='Brown')

    def test_get_all_puppies(self):
        # Add objects to API and DB, get response from API.
        response = client.get(reverse('get_post_puppies'))
        # Get objects from DB.
        puppies = Puppy.objects.all()
        # Converts puppies data into puppy objects.
        serializer = PuppySerializer(puppies, many=True)
        # Check if DB query equals API query.
        self.assertEqual(response.data, serializer.data)
        # Check if response status is 200.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetSinglePuppyTest(TestCase):
    # """ Test module for GET single puppy API """

    def setUp(self):
        self.casper = Puppy.objects.create(
            name='Casper', age=3, breed='Bull Dog', color='Black')
        self.muffin = Puppy.objects.create(
            name='Muffin', age=1, breed='Gradane', color='Brown')
        self.rambo = Puppy.objects.create(
            name='Rambo', age=2, breed='Labrador', color='Black')
        self.ricky = Puppy.objects.create(
            name='Ricky', age=6, breed='Labrador', color='Brown')

    def test_get_valid_single_puppy(self):
        response = client.get(
            reverse('get_delete_update_puppy', kwargs={'pk': self.rambo.pk}))
        puppy = Puppy.objects.get(pk=self.rambo.pk)
        serializer = PuppySerializer(puppy)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_puppy(self):
        response = client.get(
            reverse('get_delete_update_puppy', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
