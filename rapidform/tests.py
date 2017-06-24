from django.test import TestCase, override_settings
from django.shortcuts import reverse
import responses
import pkg_resources
import json


class RapidFormTest(TestCase):

    @responses.activate
    @override_settings(
        RAPIDPRO_HOST='example.org',
        RAPIDPRO_FLOW='flow',
        RAPIDPRO_TOKEN='token',
        RAPIDPRO_URN_COUNTRY_CODE='256',
        RAPIDPRO_URN_FIELD='WHPX',
        RAPIDPRO_PATTERNS=['district', 'village'],
    )
    def test_post(self):

        def cb(request):
            self.maxDiff = None
            data = json.loads(request.body)
            self.assertEqual(data, {
                "flow": 'flow',
                "urns": [
                    "tel:+256-700-000000",
                ],
                "extra": {
                    'answers': {
                        '53615006': {
                            'choice': {
                                'label': 'East Central'
                            },
                            'field': {
                                'id': '53615006',
                                'type': 'multiple_choice'
                            },
                            'type': 'choice'
                        },
                        '53615733': {
                            'choice': {
                                'label': 'Iganga'
                            },
                            'field': {
                                'id': '53615733',
                                'type': 'multiple_choice'
                            },
                            'type': 'choice'
                        },
                        'WHPX': {
                            'field': {
                                'id': 'WHPX',
                                'type': 'short_text'
                            },
                            'text': '0700000000',
                            'type': 'text'
                        },
                        'ZVQY': {
                            'choice': {
                                'label': 'VHT'
                            },
                            'field': {
                                'id': 'ZVQY',
                                'type': 'multiple_choice'
                            },
                            'type': 'choice'
                        },
                        'cO3E': {
                            'choice': {
                                'label': 'Bubenge A'
                            },
                            'field': {
                                'id': 'cO3E',
                                'type': 'dropdown'
                            },
                            'type': 'choice'
                        },
                        'kvq9': {
                            'field': {
                                'id': 'kvq9',
                                'type': 'short_text'
                            },
                            'text': 'Simon de Haan',
                            'type': 'text'
                        }
                    },
                    'patterns': {
                        'district': [{
                            'choice': {
                                'label': 'Iganga',
                            },
                            'field': {
                                'id': '53615733',
                                'type': 'multiple_choice',
                            },
                            'type': 'choice',
                        }],
                        'village': [{
                            'choice': {
                                'label': 'Bubenge A',
                            },
                            'field': {
                                'id': 'cO3E',
                                'type': 'dropdown',
                            },
                            'type': 'choice'
                        }]
                    }
                }
            })

            # From the RapidPro docs
            body = {
                "id": 150051,
                "flow": {
                    "uuid": "f5901b62-ba76-4003-9c62-72fdacc1b7b7",
                    "name": "Thrift Shop"
                },
                "groups": [
                    {
                        "uuid": "f5901b62-ba76-4003-9c62-72fdacc1b7b7",
                        "name": "Ryan & Macklemore"
                    }
                ],
                "contacts": [
                    {
                        "uuid": "f5901b62-ba76-4003-9c62-fjjajdsi15553",
                        "name": "Wanz"
                    }
                ],
                "restart_participants": True,
                "status": "complete",
                "extra": {
                    "first_name": "Ryan",
                    "last_name": "Lewis"
                },
                "created_on": "2013-08-19T19:11:21.082Z",
                "modified_on": "2013-08-19T19:11:21.082Z"
            }
            return (201, {}, json.dumps(body))

        responses.add_callback(
            responses.POST,
            "https://example.org/api/v2/flow_starts.json",
            callback=cb, content_type='application/json')

        resp = self.client.post(
            reverse('receive'),
            data=pkg_resources.resource_string('rapidform', 'fixture.json'),
            content_type='application/json')

        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(responses.calls), 1)