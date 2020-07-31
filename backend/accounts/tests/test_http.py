from random import randrange
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from ..models import MobileToken
from ..tasks import send_mobile_token


EMAIL = 'user@prueba.com'
PASSWORD = 'p4ssw0rd!'


def create_user(username=EMAIL, password=PASSWORD, role=1):
    return get_user_model().objects.create_user(
        username=username,
        email=username,
        password=password,
        mobile='+5491124004759',
        role=role,
        verified_mobile=False
    )


def token_header(user):
    return {'HTTP_AUTHORIZATION': f'Token {user.auth_token.key}'}


def create_mobile_token(user, is_expired=False):
    mobile_token = MobileToken(
        user=user,
        token=randrange(000000, 999999),
        is_expired=is_expired,
    )
    mobile_token.save()
    return mobile_token


class AuthenticationTest(APITestCase):

    def test_user_can_sign_up(self):
        response = self.client.post(reverse('signup'), data={
            'email': EMAIL,
            'first_name': 'Pedro',
            'last_name': 'Perez',
            'mobile': '+5491124001111',
            'role': 1,
            'password1': PASSWORD,
            'password2': PASSWORD
        })
        user = get_user_model().objects.last()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['email'], user.email)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)
        self.assertEqual(response.data['mobile'], user.mobile)
        self.assertEqual(response.data['role'], user.role)

    def test_user_can_login(self):
        user = create_user()
        response = self.client.post(reverse('login'), data={
            'username': user.username,
            'password': PASSWORD
        })
        self.assertEqual(response.data['email'], user.email)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)
        self.assertEqual(response.data['mobile'], user.mobile)
        self.assertEqual(response.data['role'], user.role)
        self.assertEqual(response.data['token'], user.auth_token.key)

    def test_user_can_logout(self):
        user = create_user()
        response = self.client.post(
            reverse('logout'),
            **token_header(user),
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_user_can_retrieve(self):
        user = create_user()
        response = self.client.get(
            reverse('user-info', kwargs={'pk': user.pk}),
            **token_header(user))
        self.assertEqual(status.HTTP_200_OK,
                         response.status_code)

    def test_user_can_modify(self):
        user = create_user()
        response = self.client.patch(
            reverse('user-info', kwargs={'pk': user.pk}),
            **token_header(user),
            data={
                'mobile': '+541124004455',
            }
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT,
                         response.status_code)
        self.assertNotEqual(user.get_mobile(),
                            response.data['mobile'])

    def test_create_mobile_token(self):
        user = create_user()
        response = self.client.post(
            reverse('mobile-token'),
            **token_header(user)
        )
        self.assertEqual(status.HTTP_201_CREATED,
                         response.status_code)

    def test_validate_mobile(self):
        user = create_user()
        db_mobile_token = create_mobile_token(user)
        response = self.client.patch(
            reverse('mobile-token'),
            **token_header(user),
            data={
                'token': db_mobile_token.token
            }
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

