# -*- coding: utf-8 -*-
""" Unittests for password_required app. """

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.test import TestCase

class LoginViewTest(TestCase):
    """ Tests for the login view """
    urls = 'password_required.test_urls'

    def setUp(self):
        """ Configure the testcase """
        self.login_url = reverse('password_required.views.login')
        settings.PASSWORD_REQUIRED_PASSWORD = u'prøve'

    def test_form_display(self):
        """ Test that the login form is rendered. """
        response = self.client.get(self.login_url, {
            REDIRECT_FIELD_NAME: '/test',
        })
        self.assertTemplateUsed(response,
                                template_name='password_required_login.html')

