RapidPro TypeForm Relay
=======================

Environment variables:

- DEBUG
- SECRET_KEY
- RAPIDPRO_HOST
- RAPIDPRO_TOKEN
- RAPIDPRO_FLOW
- RAPIDPRO_URN_COUNTRY_CODE
- RAPIDPRO_URN_FIELD
- RAPIDPRO_PATTERNS comma delimited patterns to be extracted: "district,village"

Patterns are matched case-insensitively and return the full answer dictionaries for
any field definition where the pattern is in the title.

Google's phonenumbers library is used to validate the URN_COUNTRY_CODE + URN_FIELD value
to make sure the URN submitted to RapidPro is valid.

Results in the following being posted to::

    https://RAPIDPRO_HOST/api/v2/flow_starts.json

With payload::

    flow: <RAPIDPRO_FLOW>
    urns: ['tel:+<validated urn>']
    extra: {
        answers: {
            '<field id>': {
                'choice': {
                    'label': 'East Central'
                },
                'field': {
                    'id': '<field id>',
                    'type': 'multiple_choice'
                },
                'type': 'choice'
            },
            '<field id>': {
                'field': {
                    'id': '<field id>',
                    'type': 'short_text'
                },
                'text': '0700000000',
                'type': 'text'
            },
            '<field id>': {
                'choice': {
                    'label': 'Bubenge A'
                },
                'field': {
                    'id': '<field id>',
                    'type': 'dropdown'
                },
                'type': 'choice'
            },
        },
        patterns: {
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

