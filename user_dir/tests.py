import json
from unittest.mock import patch
from graphene_django.utils.testing import GraphQLTestCase
from django.test import Client
from django.contrib.auth import get_user_model


class APITestCase(GraphQLTestCase):
    GRAPHQL_URL = "/users/graphql"
    client = Client()

    # Setup data for the tests
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(email='test@example.com', password='testpassword')

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
        self.assertEqual(content['data']['profile']['email'], self.user.email)


class APITestCaseWithoutLogin(GraphQLTestCase):
    GRAPHQL_URL = "/users/graphql"

    def setUp(self):
        # Clear any existing users
        get_user_model().objects.all().delete()

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

        mock_cache_set.side_effect = lambda key, value, timeout: cache.update({key: value})
        mock_cache_get.side_effect = cache.get

        # Test the register mutation
        response = self.query(
            '''mutation { register(email: "newuser@example.com", password: "newpassword", 
            verifyCode: "123456") { success errors { email verifyCode } } }'''
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

        # Check that registration was successful
        self.assertTrue(content['data']['register']['success'])
        self.assertIsNone(content['data']['register']['errors'])

        # Test registration with existing email
        response = self.query(
            '''mutation { register(email: "newuser@example.com", password: "newpassword", 
            verifyCode: "123456") { success errors { email verifyCode } } }'''
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertFalse(content['data']['register']['success'])
        self.assertEqual(content['data']['register']['errors']['email'], 'Email already exists.')

    @patch('user_dir.tasks.send_email.delay',
           side_effect=lambda email, subject, template, context: None)
    def test_send_verify_email_mutation(self, mock_send_email):
        # Test successful sending of verification email
        response = self.query(
            '''
            mutation {
                sendVerifyEmail(email: "newuser@example.com") {
                    success
                    errors {
                        email
                    }
                }
            }
            '''
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['sendVerifyEmail']['success'])
        self.assertIsNone(content['data']['sendVerifyEmail']['errors'])

        # Create a user
        get_user_model().objects.create_user(email='newuser@example.com', password='newpassword')

        # Test sending of verification email to existing email
        response = self.query(
            '''
            mutation {
                sendVerifyEmail(email: "newuser@example.com") {
                    success
                    errors {
                        email
                    }
                }
            }
            '''
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertFalse(content['data']['sendVerifyEmail']['success'])
        self.assertEqual(content['data']['sendVerifyEmail']['errors']['email'],
                         'Email already exists.')

    def test_login_mutation(self):
        get_user_model().objects.create_user(email='newuser@example.com', password='newpassword')

        # Test successful login
        response = self.query(
            '''
            mutation {
                login(email: "newuser@example.com", password: "newpassword") {
                    payload
                    refreshExpiresIn
                }
            }
            '''
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['login']['payload']['email'], 'newuser@example.com')

        # Test login with wrong password
        response = self.query(
            '''
            mutation {
                login(email: "newuser@example.com", password: "wrongpassword") {
                    payload
                    refreshExpiresIn
                }
            }
            '''
        )
        content = json.loads(response.content)

        self.assertEqual(len(content['errors']), 1)
        self.assertEqual(content['errors'][0]['message'], 'Please enter valid credentials')
        self.assertIsNone(content['data']['login'])
