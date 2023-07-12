import json
from unittest.mock import patch
from graphene_django.utils.testing import GraphQLTestCase
from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model


class TestCase(GraphQLTestCase):
    GRAPHQL_URL = "/users/graphql/"
    client = Client()

    # Setup data for the tests
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        User = get_user_model()
        cls.user = User.objects.create_user(email='test@example.com', password='testpassword')

    def setUp(self):
        # Log in the user
        self.client.login(email='test@example.com', password='testpassword')

    # Test the profile query
    def test_profile_query(self):
        response = self.query(
            '''
            query {
                profile {
                    email
                }
            }
            '''
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertEquals(content['data']['profile']['email'], self.user.email)

    # Test the register mutation
    @patch('django.core.cache.cache.set')
    @patch('django.core.cache.cache.get')
    @patch('user_dir.tasks.send_email.delay',
           side_effect=lambda email, subject, template, context: None)
    def test_register_mutation(self, mock_cache_set, mock_cache_get, mock_send_email):
        # Create a temporary "cache"
        cache = {}

        # Generate a verify code and save it to the "cache"
        verify_code = '123456'
        email = 'newuser@example.com'
        cache_key = f'{email}_register'
        cache[cache_key] = verify_code

        # Mock cache.set and cache.get to use the temporary "cache"
        mock_cache_set.side_effect = lambda key, value, timeout: cache.update({key: value})
        mock_cache_get.side_effect = lambda key: cache.get(key)

        # Test the register mutation
        response = self.query(
            '''
            mutation {
                register(email: "newuser@example.com", password: "newpassword", verifyCode: "123456") {
                    success
                    errors {
                        email
                        verifyCode
                    }
                }
            }
            '''
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

        # Check that registration was successful
        self.assertTrue(content['data']['register']['success'])
        self.assertIsNone(content['data']['register']['errors'])


