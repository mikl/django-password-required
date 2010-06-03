# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^password_required/$', 'password_required.views.login'),

    # We just need a 200 response code, never mind that the template
    # produces no output without a context.
    (r'^test/$', 'django.views.generic.simple.direct_to_template', {
        'template': 'password_required_login.html',
    }),
)

