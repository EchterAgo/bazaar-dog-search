from django import forms
from django.utils.translation import ugettext as _

class TruthyWidget(forms.Select):
    """Convert true/false values into the internal Python True/False.
    This can be used for AJAX queries that pass true/false from JavaScript's
    internal types through.
    """
    def __init__(self, attrs=None):
        choices = (('', _('Unknown')),
                   ('true', _('Yes')),
                   ('false', _('No')))
        super().__init__(attrs, choices)

    def render(self, name, value, attrs=None):
        try:
            value = {
                True: 'true',
                '': 'false',
                '1': 'true',
                '': 'false'
            }[value]
        except KeyError:
            value = ''
        return super().render(name, value, attrs)

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        if isinstance(value, str):
            value = value.lower()

        return {
            '1': True,
            '0': '',
            'true': True,
            'false': '',
            True: True,
            False: '',
        }.get(value, None)

class FalsyWidget(forms.Select):
    """Convert true/false values into the internal Python True/False.
    This can be used for AJAX queries that pass true/false from JavaScript's
    internal types through.
    """
    def __init__(self, attrs=None):
        choices = (('', _('Unknown')),
                   ('true', _('Yes')),
                   ('false', _('No')))
        super().__init__(attrs, choices)

    def render(self, name, value, attrs=None):
        try:
            value = {
                None: 'false',
                True: 'true',
                '': 'false',
                '1': 'true',
                '': 'false'
            }[value]
        except KeyError:
            value = ''
        return super().render(name, value, attrs)

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        if isinstance(value, str):
            value = value.lower()

        return {
            '1': True,
            '0': '',
            'true': True,
            'false': '',
            True: True,
            False: '',
        }.get(value, None)