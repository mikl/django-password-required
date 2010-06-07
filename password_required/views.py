# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.models import Site, RequestSite
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from password_required.forms import AuthenticationForm

@csrf_protect
@never_cache
def login(request, template_name='password_required_login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm):
    """Displays the login form and handles the login action."""
    redirect_to = _clean_redirect(request.REQUEST.get(redirect_field_name, ''))

    # If the user is already logged in, redirect him immediately.
    if request.session.get('password_required_auth', False):
        return HttpResponseRedirect(redirect_to)

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            # Mark the user as logged in via his session data.
            request.session['password_required_auth'] = True

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)

    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)

    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))

def _clean_redirect(redirect_to):
    """
    Perform a few security checks on the redirect destination.

    Copied from django.contrib.auth.views.login. It really should be split
    out from that.
    """
    # Light security check -- make sure redirect_to isn't garbage.
    if not redirect_to or ' ' in redirect_to:
        redirect_to = settings.LOGIN_REDIRECT_URL

    # Heavier security check -- redirects to http://example.com should 
    # not be allowed, but things like /view/?param=http://example.com 
    # should be allowed. This regex checks if there is a '//' *before* a
    # question mark.
    elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
            redirect_to = settings.LOGIN_REDIRECT_URL

    return redirect_to

