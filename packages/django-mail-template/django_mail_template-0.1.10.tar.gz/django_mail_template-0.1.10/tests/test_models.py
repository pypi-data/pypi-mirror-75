# -*- coding: UTF-8 -*-
from unittest.mock import patch, call

import pytest
from unittest import TestCase as UnitTestCase
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.db import models
from django_mail_template.models import (MailTemplate, Configuration)


@pytest.mark.django_db
class TestMailTemplate(UnitTestCase):

    def setUp(self) -> None:
        self.mail = MailTemplate(title=_('test title'),
                                 from_email='a@b.com',
                                 subject=_('test subject'))

    def test_mail_data_model(self):
        assert isinstance(self.mail, models.Model)

    def test_required_fields(self):
        self.mail.full_clean()  # Should not fail

    def test_mail_string(self):
        expected_text = _('test title')
        self.assertEqual(expected_text, str(self.mail))

    def test_mail_template_verbose_name(self):
        verbose_name = MailTemplate._meta.verbose_name
        assert verbose_name == _('Mail Template')

    def test_mail_template_plural_name(self):
        verbose_name = MailTemplate._meta.verbose_name_plural
        assert verbose_name == _('Mails Templates')

    def test_title_field_type(self):
        field = MailTemplate._meta.get_field('title')
        assert isinstance(field, models.CharField)

    def test_title_field_max_length(self):
        big_subject = 'chars' * 20 + 'exceed'  # 5 * 20 = 100 character max
        subject_ok = 'chars' * 20
        self.mail.title = big_subject
        with self.assertRaises(ValidationError):
            self.mail.full_clean()
        self.mail.title = subject_ok
        self.mail.full_clean()

    def test_title_verbose_name(self):
        field = MailTemplate._meta.get_field('title')
        self.assertEqual(field.verbose_name, _("Title"))

    def test_title_field_help_text(self):
        expected_help_text = \
            _('A title to identify the mail template.')
        actual_help_text = MailTemplate._meta.get_field('title').help_text
        self.assertEqual(expected_help_text, actual_help_text)

    def test_to_field_max_length(self):
        lots = 'addressmailtest@mail.com,' * 41  # 25 character * 41 == 1025
        self.mail.to = lots[:-1]
        with self.assertRaises(ValidationError):
            self.mail.full_clean()
        ok = 'addressmailtest@mail.com,' * 40  # 25 character * 40 = 1000
        self.mail.to = ok[:-1]
        self.mail.full_clean()

    def test_to_field_verbose_name(self):
        expected = _('To')
        actual = MailTemplate._meta.get_field('to').verbose_name
        self.assertEqual(expected, actual)

    def test_to_field_help_text(self):
        expected_help_text = \
            _('A list with email addresses separated with coma.')
        actual_help_text = MailTemplate._meta.get_field('to').help_text
        self.assertEqual(expected_help_text, actual_help_text)

    def test_to_field_do_validation(self):
        self.mail.to = 'no-mail, simple@mail.com'
        with self.assertRaises(ValidationError) as e:
            self.mail.full_clean()
        exception = e.exception
        self.assertEqual(
            exception.messages[0],
            _('Enter a valid comma separated list of email addresses for '
              'field To.'))

    def test_cc_field_verbose(self):
        expected = _('Copy to')
        actual = MailTemplate._meta.get_field('cc').verbose_name
        self.assertEqual(expected, actual)

    def test_cc_field_help_text(self):
        expected_help_text = \
            _('A list with email addresses separated with coma '
              'to be used in the "Cc" header.')
        actual_help_text = MailTemplate._meta.get_field('cc').help_text
        self.assertEqual(expected_help_text, actual_help_text)

    def test_cc_field_max_length(self):
        lots = 'addressmailtest@mail.com,' * 41  # 25 character * 41 == 1025
        self.mail.cc = lots[:-1]
        with self.assertRaises(ValidationError):
            self.mail.full_clean()
        ok = 'addressmailtest@mail.com,' * 40  # 25 character * 40 = 1000
        self.mail.cc = ok[:-1]
        self.mail.full_clean()

    def test_cc_field_do_validation(self):
        self.mail.cc = 'no-mail, simple@mail.com'
        with self.assertRaises(ValidationError) as e:
            self.mail.full_clean()
        exception = e.exception
        self.assertEqual(
            exception.messages[0],
            _('Enter a valid comma separated list of email addresses for '
              'field Copy.'))

    def test_bcc_field_verbose_name(self):
        expected = _('Blind copy')
        actual = MailTemplate._meta.get_field('bcc').verbose_name
        self.assertEqual(expected, actual)

    def test_bcc_field_help_text(self):
        expected_help_text = \
            _('A list with email addresses separated with coma to be '
              'used in the "Bcc" header.')
        actual_help_text = MailTemplate._meta.get_field('bcc').help_text
        self.assertEqual(expected_help_text, actual_help_text)

    def test_bcc_field_max_length(self):
        lots = 'addresmail_test@mail.com,' * 41  # 25 character * 41 == 1025
        self.mail.bcc = lots[:-1]
        with self.assertRaises(ValidationError):
            self.mail.full_clean()
        ok = 'addresmail_test@mail.com,' * 40  # 25 character * 40 = 1000
        self.mail.bcc = ok[:-1]
        self.mail.full_clean()

    def test_bcc_field_do_validation(self):
        self.mail.bcc = 'no-mail, simple@mail.com'
        with self.assertRaises(ValidationError) as e:
            self.mail.full_clean()
        exception = e.exception
        self.assertEqual(
            exception.messages[0],
            _('Enter a valid comma separated list of email addresses for '
              'field Blind copy.'))

    def test_from_email_field_max_length(self):
        lots = 'a' * 250 + 'addressmailtest@mail.com'
        self.mail.from_email = lots[:-1],
        with self.assertRaises(ValidationError):
            self.mail.full_clean()
        self.mail.from_email = 'a' * 225 + 'addressmailtest@mail.com'
        self.mail.full_clean()

    def test_from_email_field_verbose_name(self):
        expected = _('From')
        actual = MailTemplate._meta.get_field('from_email').verbose_name
        self.assertEqual(expected, actual)

    def test_from_email_field_help_text(self):
        expected_help_text = _("Sender's email address.")
        actual_help_text = MailTemplate._meta.get_field('from_email').help_text
        self.assertEqual(expected_help_text, actual_help_text)

    def test_reply_to_field_verbose_name(self):
        expected = _('Reply to')
        actual = MailTemplate._meta.get_field('reply_to').verbose_name
        self.assertEqual(expected, actual)

    def test_reply_to_field_help_text(self):
        expected_help_text = \
            _('A list with email addresses separated with coma to be '
              'used in the "Reply-To" header.')
        actual_help_text = MailTemplate._meta.get_field('reply_to').help_text
        self.assertEqual(expected_help_text, actual_help_text)

    def test_reply_to_field_max_length(self):
        lots = 'addresmail_test@mail.com,' * 41  # 25 character * 41 == 1025
        self.mail.reply_to = lots[:-1]
        with self.assertRaises(ValidationError):
            self.mail.full_clean()
        ok = 'addresmail_test@mail.com,' * 40  # 25 character * 40 = 1000
        self.mail.reply_to = ok[:-1]
        self.mail.full_clean()

    def test_reply_to_do_validation(self):
        self.mail.reply_to = 'no-mail, simple@mail.com'
        with self.assertRaises(ValidationError) as e:
            self.mail.full_clean()
        exception = e.exception
        self.assertEqual(
            exception.messages[0],
            _('Enter a valid comma separated list of email addresses for '
              'field Reply to.'))

    def test_subject_field_max_length(self):
        big_subject = 'c' * 140 + 'exceed'  # 1 * 140 = 140 character max
        subject_ok = 'c' * 140
        self.mail.subject = big_subject
        with self.assertRaises(ValidationError):
            self.mail.full_clean()
        self.mail.subject = subject_ok
        self.mail.full_clean()

    def test_subject_field_verbose_name(self):
        expected = _('Subject')
        actual = MailTemplate._meta.get_field('subject').verbose_name
        self.assertEqual(expected, actual)

    def test_subject_field_help_text(self):
        expected_help = _('Subject text for the mail. Context variable can be '
                          'used.')
        actual_help_text = MailTemplate._meta.get_field('subject').help_text
        self.assertEqual(expected_help, actual_help_text)

    def test_body_field_verbose_name(self):
        expected = _('Body')
        actual = MailTemplate._meta.get_field('body').verbose_name
        self.assertEqual(expected, actual)

    def test_body_field_help_text(self):
        expected_help_text = _('The content of the mail. Context variable can '
                               'be used.')
        actual_help_text = MailTemplate._meta.get_field('body').help_text
        self.assertEqual(expected_help_text, actual_help_text)

    def test_body_field_type(self):
        field = MailTemplate._meta.get_field('body')
        assert isinstance(field, models.TextField)

    def test_body_field_max_length(self):
        """
        Just a test to check it can hold at least 50000 characters
        """
        big_body = 'chars' * 10000 + 'exceed'
        self.mail.body = big_body
        self.mail.full_clean()

    def test_description_field_type(self):
        field = MailTemplate._meta.get_field('description')
        assert isinstance(field, models.TextField)

    def test_description_verbose_name(self):
        field = MailTemplate._meta.get_field('description')
        self.assertEqual(field.verbose_name, _("Description"))

    def test_description_help_test(self):
        field = MailTemplate._meta.get_field('description')
        self.assertEqual(
            field.help_text,
            _("Description of the mail template."))


class TestSendMailTemplate(UnitTestCase):

    def setUp(self) -> None:
        self.mail = MailTemplate(from_email='a@b.com',
                                 subject=_('Hello {test}'))
        self.mail.body = _('Test text using {test}')
        self.mail.to = ['b@c.com']
        self.context_data = {'test': 'test_value'}

    @patch('django_mail_template.models.replace_context_variable')
    def test_subject_replace_context_variables(
            self, mock_replace_context_variable
    ):
        self.mail.send(self.context_data)
        assert call(text='Hello {test}', context_variable=self.context_data) \
               in mock_replace_context_variable.call_args_list

    @patch('django_mail_template.models.replace_context_variable')
    def test_body_replace_context_variables(
            self, mock_replace_context_variable
    ):
        self.mail.send(self.context_data)
        assert call(text='Hello {test}', context_variable=self.context_data) \
               in mock_replace_context_variable.call_args_list

    @patch('django_mail_template.models.replace_context_variable')
    def test_replace_context_variables_was_called_twice(
            self, mock_replace_context_variable
    ):
        self.mail.send(self.context_data)
        assert 2 == mock_replace_context_variable.call_count

    @patch('django_mail_template.models.EmailMultiAlternatives.send')
    def test_can_send_mail_without_context(
            self, mock_django_mail
    ):
        self.mail.send()
        assert 1 == mock_django_mail.call_count

    @patch('django_mail_template.models.EmailMultiAlternatives.send')
    def test_can_not_send_mail_without_required_attributes_valid_context(
            self, mock_django_mail
    ):
        with self.assertRaises(ValueError) as e:
            self.mail.send('fake-context')
        exception = e.exception
        self.assertEqual(
            str(exception),
            'The argument for send method must be a mapping.')
        assert 0 == mock_django_mail.call_count

    @patch('django_mail_template.models.clean_address_list')
    def test_send_mail_convert_to_field(
            self, mock_clean_address_list
    ):
        expected = [call(self.mail.to), call(self.mail.cc),
                    call(self.mail.bcc), call(self.mail.reply_to)]
        self.mail.send()
        self.assertEqual(mock_clean_address_list.call_args_list, expected)


class TestConfiguration(UnitTestCase):
    """
    Store dynamic configuration data used to set up django_mail_template.

    Builtin key process:

    * 'LOG_MAIL_ACTIVITY': A configuration with this value in process attribute
      will configure django_mail_template to log mail activity.?????
    """
    def setUp(self) -> None:
        self.configuration = Configuration(
            process='PROCESS_ID'
        )

    def test_configuration_verbose_name(self):
        verbose_name = Configuration._meta.verbose_name
        assert verbose_name == _('Configuration')

    def test_configuration_plural_name(self):
        verbose_name = Configuration._meta.verbose_name_plural
        assert verbose_name == _('Configurations')

    def test_required_fields(self):
        self.configuration.full_clean()

    def test_model_type_for_configuration(self):
        assert isinstance(self.configuration, models.Model)

    def test_process_field_type(self):
        field = Configuration._meta.get_field('process')
        assert isinstance(field, models.CharField)

    def test_process_field_max_length(self):
        big_data = 'chars' * 40 + 'exceed'
        data_ok = 'chars' * 40
        self.configuration.process = big_data
        with self.assertRaises(ValidationError):
            self.configuration.full_clean()
        self.configuration.process = data_ok
        self.configuration.full_clean()

    def test_process_verbose_name(self):
        field = Configuration._meta.get_field('process')
        self.assertEqual(field.verbose_name, _("Process"))

    def test_process_field_help_text(self):
        expected_help_text = \
            _('A name to identify the process.')
        actual_help_text = Configuration._meta.get_field('process').help_text
        self.assertEqual(expected_help_text, actual_help_text)

    def test_mail_template_field_type(self):
        field = Configuration._meta.get_field('mail_template')
        assert isinstance(field, models.ForeignKey)

    def test_mail_template_filed_point_to_right_data_model(self):
        field = Configuration._meta.get_field('mail_template')
        assert field.related_model == MailTemplate

    def test_mail_template_verbose_name(self):
        field = Configuration._meta.get_field('mail_template')
        self.assertEqual(field.verbose_name, _("Mail template"))

    def test_mail_template_field_help_text(self):
        expected_help_text = \
            _('The mail template linked with this configuration (process). '
              'When required a mail template to this configurations this '
              'mail template will be returned.')
        actual_help_text = Configuration._meta.get_field(
            'mail_template').help_text
        self.assertEqual(expected_help_text, actual_help_text)

    def test_configuration_string_without_mail_template(self):
        expected_text = 'PROCESS_ID - ' + _('No mail template')
        assert str(self.configuration) == expected_text

    def test_configuration_string_with_mail_template(self):
        # Fixture
        mail = MailTemplate.objects.create(
            title='Title for mail template',
            subject='test mail template subject',
            from_email='a@b.com'
        )
        self.configuration.mail_template = mail
        expected_text = _('PROCESS_ID - Title for mail template')
        assert str(self.configuration) == expected_text

    def test_description_field_type(self):
        field = Configuration._meta.get_field('description')
        assert isinstance(field, models.TextField)

    def test_description_verbose_name(self):
        field = Configuration._meta.get_field('description')
        self.assertEqual(field.verbose_name, _("Description"))

    def test_description_help_test(self):
        field = Configuration._meta.get_field('description')
        self.assertEqual(
            field.help_text,
            _("Description for configuration. This description can contain "
              "the contextual variables that are expected to be used in "
              "associated MailTemplates."))


class TestConfigurationBehavior(UnitTestCase):

    def setUp(self) -> None:
        self.configuration = Configuration(process='TestProcess')

    def test_get_mail_template_return_none_without_mail_template(self):
        assert Configuration.get_mail_template('') is None

    def test_get_mail_template_return_correct_mail_template(self):
        # Fixture
        mail_yes = MailTemplate.objects.create(
            title='Title for correct mail template',
            subject='test mail template subject',
            from_email='a@b.com'
        )
        mail_no = MailTemplate.objects.create(
            title='Title for incorrect mail template',
            subject='Bad mail template subject',
            from_email='a@b.com'
        )
        configuration = Configuration(process='Fake_process')
        configuration.mail_template = mail_no
        configuration.save()
        self.configuration.mail_template = mail_yes
        self.configuration.save()

        assert Configuration().get_mail_template('TestProcess') == mail_yes
