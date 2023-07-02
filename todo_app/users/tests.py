from django.test import TestCase

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UsersViewsTestCase(TestCase):
    TODO_INDEX_URL = "/todo/"
    REGISTER_URL = "/users/register/"

    def setUp(self):
        pass

    def test_register_returns_empty_form_when_not_post_request(self):
        response = self.client.get(self.REGISTER_URL)

        self.assertEquals(response.status_code, 200)
        self.assertTrue(isinstance(response.context["form"], UserCreationForm))

    def test_register_creates_new_user_when_request_post_and_valid_data(self):
        username = "TestUser1"
        password = "TestUser1Password_"

        form_data = {
            "username": username,
            "password1": password,
            "password2": password,
        }

        response = self.client.post(self.REGISTER_URL, data=form_data)

        self.assertRedirects(response, self.TODO_INDEX_URL)

        dne = False
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            dne = True

        self.assertFalse(dne)

    def test_register_returns_form_with_errors_when_invalid_data(self):
        invalid_username = "!!!"
        password = "TestUser1Password_"

        form_data = {
            "username": "",
            "password1": password,
            "password2": password,
        }

        response = self.client.post(self.REGISTER_URL, data=form_data)
        self.assertFormError(response, "form", "username", "This field is required.")

        dne = False
        try:
            User.objects.get(username=invalid_username)
        except User.DoesNotExist:
            dne = True

        self.assertTrue(dne)
