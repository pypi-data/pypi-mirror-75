from django.apps import apps
from django.test import TestCase
from django_mail_template.apps import DjangoMailTemplateConfig


class DjangoMailTemplateConfigTest(TestCase):

    def test_apps(self):
        # Test the class
        self.assertEqual(DjangoMailTemplateConfig.name, 'django_mail_template')
        self.assertEqual(DjangoMailTemplateConfig.verbose_name,
                         'Django Mail Template')

        # Test the app
        self.assertEqual(apps.get_app_config('django_mail_template').name,
                         'django_mail_template')
