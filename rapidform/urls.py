"""rapidform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse
from django.views import View
from collections import defaultdict

import json
import phonenumbers
from temba_client.v2 import TembaClient

import logging

logger = logging.getLogger(__name__)


class ReceiveView(View):

    def __init__(self):
        self.client = TembaClient(
            settings.RAPIDPRO_HOST,
            settings.RAPIDPRO_TOKEN)

    def get(self, request):
        return HttpResponse('Only POST allowed')

    def post(self, request):
        data = json.loads(request.body)
        logger.info('Received: %r' % (data,))

        answers = dict([
            (answer['field']['id'], answer)
            for answer in data['form_response']['answers']])

        matches = defaultdict(list)
        for pattern in settings.RAPIDPRO_PATTERNS:
            for field in data['form_response']['definition']['fields']:
                if pattern.lower() in field['title'].lower():
                    matches[pattern.lower()].append(answers[field['id']])

        urns = [
            phonenumbers.PhoneNumber(
                settings.RAPIDPRO_URN_COUNTRY_CODE,
                answers[settings.RAPIDPRO_URN_FIELD]['text'])]

        self.client.create_flow_start(
            flow=settings.RAPIDPRO_FLOW,
            urns=[
                phonenumbers.format_number(
                    urn, phonenumbers.PhoneNumberFormat.RFC3966)
                for urn in urns
            ],
            extra={
                'answers': answers,
                'patterns': matches,
            })
        return HttpResponse()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', csrf_exempt(ReceiveView.as_view()), name='receive')
]
