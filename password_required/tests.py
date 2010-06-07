# -*- coding: utf-8 -*-
""" Unittests for password_required app. """

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

class MissingConfTest(TestCase):
    """ Tests for correct behavior on missing configuration. """
    urls = 'password_required.test_urls'

    def setUp(self):
        """ Configure the testcase """
        self.login_url = reverse('password_required.views.login')

        # Unset the password if set.
        try:
            delattr(settings, 'PASSWORD_REQUIRED_PASSWORD')
        except AttributeError:
            print 'durrr'
            pass

    def test_missing_password_fail(self):
        """ Test that the login form fails when the password is not set. """
        response = self.client.post(self.login_url, {
            REDIRECT_FIELD_NAME: '/test/',
            'password': u'prøve'
        })

        self.assertFormError(response, 'form', 'password',
                             _("PASSWORD_REQUIRED_PASSWORD is not set, and thus it is currently impossible to log in."))

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
            REDIRECT_FIELD_NAME: '/test/',
        })
        self.assertTemplateUsed(response,
                                template_name='password_required_login.html')

    def test_successful_login(self):
        """
        Test that the login page works.
        """
        response = self.client.post(self.login_url, {
            REDIRECT_FIELD_NAME: '/test/',
            'password': u'prøve'
        })

        self.assertRedirects(response, '/test/')

        # Visiting the login page after successfully logging in, should
        # cause an immediate redirect.
        response = self.client.get(self.login_url, {
            REDIRECT_FIELD_NAME: '/test/',
        })
        self.assertRedirects(response, '/test/')

