from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from .serializers import TenantReviewListSerializer

from .models import TenantReview
from users.models import TenantProfile, LandlordProfile
from property.models import Property
from property.factories import CityFactory


class TenantReviewTestCases(APITestCase):
    def setUp(self) -> None:
        self.client_ = User.objects.create_user(username='test', password='12345')
        self.client1_ = User.objects.create_user(username='test1', password='12345')
        self.city = CityFactory()
        self.review_on = TenantProfile.objects.create(
            user=self.client_,
            firstname='Name',
            lastname='Lastname',
            middlename='Middlename',
            birth_date='1990-06-28',
        )
        self.landlord = LandlordProfile.objects.create(
            user=self.client1_,
            firstname='Name',
            lastname='Lastname',
            middlename='Middlename',
            birth_date='1990-06-28',
        )
        self.prop = Property.objects.create(landlord=self.landlord, name='my property1', address='my address1',
                                                 description='no description1', city=self.city)
        self.data = {'title': 'title', 'description': 'description', 'rating': 4,
                     'reviewer': self.prop.pk, 'review_on': self.review_on.pk}
        self.incorrect_data = {'title': 'title', 'description': 'description', 'rating': 0}
        self.tenant_review = TenantReview.objects.create(
            title=self.data['title'],
            description=self.data['description'],
            rating=self.data['rating'],
            reviewer=self.prop,
            review_on=self.review_on
        )
        self.client.login(username='test', password='12345')
        self.client.login(username='test1', password='12345')

    def test_create_tenant_review(self):
        tenant_review = self.client.post(reverse('reviews:create-tenant-review'), self.data)
        self.assertEqual(tenant_review.status_code, status.HTTP_201_CREATED)

    def test_view_tenant_review(self):
        response = self.client.get(reverse('reviews:list-tenant-review'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_certain_tenant_review(self):
        tenant_review = self.tenant_review
        response = self.client.get(reverse('reviews:delete-update-retrieve-tenant-review',
                                           kwargs={'pk': tenant_review.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_tenant_review(self):
        tenant_review = self.tenant_review
        response = self.client.delete(reverse('reviews:delete-update-retrieve-tenant-review',
                                              kwargs={'pk': tenant_review.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_tenant_review(self):
        tenant_review = self.tenant_review
        new_data = {'description': 'really_new_description', 'rating': 5}
        response = self.client.patch(reverse('reviews:delete-update-retrieve-tenant-review',
                                             kwargs={'pk': tenant_review.pk}), data=new_data)

        self.assertEqual(response.data['description'], new_data['description'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_review_with_wrong_rating(self):
        response = self.client.post(reverse('reviews:create-tenant-review'), self.incorrect_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_tenant_review_list_model_data(self):
        self.client.post(reverse('reviews:create-tenant-review'), self.data)
        self.client.post(reverse('reviews:create-tenant-review'), self.data)
        response = self.client.get(reverse('reviews:list-tenant-review'))
        reviews = TenantReview.objects.all()
        serializer = TenantReviewListSerializer(reviews, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
