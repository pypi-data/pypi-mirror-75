# -*- coding: UTF-8 -*-
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext
from ckeditor.fields import RichTextField
from django_mail_template.tools import (replace_context_variable,
                                        clean_address_list)


class MailTemplate(models.Model):
    #: Title for mail template
    title = models.CharField(
        verbose_name=_('Title'), max_length=100,
        help_text=_('A title to identify the mail template.'))
    #: Field with destiny email address.
    to = models.CharField(
        verbose_name=_('To'), max_length=1000, blank=True, null=True,
        help_text=_('A list with email addresses separated with coma.')
    )
    #: Field with email's destinies to be copied.
    cc = models.CharField(
        verbose_name=_('Copy to'), max_length=1000, blank=True, null=True,
        help_text=_('A list with email addresses separated with coma '
                    'to be used in the "Cc" header.'))
    #: Field with email's destinies to be blind copied.
    bcc = models.CharField(
        verbose_name=_('Blind copy'), max_length=1000, blank=True, null=True,
        help_text=_('A list with email addresses separated with coma to be '
                    'used in the "Bcc" header.'))
    #: Field with sender (from) email address.
    from_email = models.EmailField(
        verbose_name=_('From'), help_text=_("Sender's email address."))
    #: Subject for the mail. Context variable can be used
    subject = models.CharField(
        verbose_name=_('Subject'), max_length=140,
        help_text=_('Subject text for the mail. Context variable can be used.')
    )

    body = RichTextField(
        verbose_name=_('Body'), blank=True, null=True,
        help_text=_('The content of the mail. Context variable can be '
                    'used.'))

    #: Field with email's reply to.
    reply_to = models.CharField(
        verbose_name=_('Reply to'), max_length=1000, blank=True, null=True,
        help_text=_('A list with email addresses separated with coma to be '
                    'used in the "Reply-To" header.'))
    description = models.TextField(
        verbose_name=_('Description'), blank=True, null=True,
        help_text=_('Description of the mail template.'))

    class Meta:
        verbose_name = _('Mail Template')
        verbose_name_plural = _('Mails Templates')

    def __str__(self):
        return self.title

    def clean(self):
        if self.to:
            clean_address_list(self.to, _('To'))
        if self.cc:
            clean_address_list(self.cc, _('Copy'))
        if self.bcc:
            clean_address_list(self.bcc, _('Blind copy'))
        if self.reply_to:
            clean_address_list(self.reply_to, _('Reply to'))

    def send(self, context=None):
        """
        When sending an email a set of attributes will be required.

        The required attributes are mainly dictated by django.core.mail
        used to send mail:
        * Message or body.
        * Subject.
        * Recipients list or to.
        * From email

        :param context: A dictionary with context variables to be used with
                        the subject and the message.
        :return: A tuple (result, message) where result is a boolean indicating
                 if mail could be sent or not. An a message in case the mail
                 could not be sent the message will be the reason. This could
                 have future uses if logging is implemented.
        """
        subject = self.subject
        body = self.body
        if context is None:
            # Needed whe no context is received so no replacement is tried.
            pass
        elif not isinstance(context, dict):
            raise ValueError(_('The argument for send method must be a '
                               'mapping.'))
        else:
            subject = replace_context_variable(text=self.subject,
                                               context_variable=context)
            body = replace_context_variable(text=self.body,
                                            context_variable=context)
        msg = EmailMultiAlternatives(
            subject=subject,
            from_email=self.from_email,
            to=clean_address_list(self.to),
            cc=clean_address_list(self.cc),
            bcc=clean_address_list(self.bcc),
            reply_to=clean_address_list(self.reply_to)
        )
        msg.body = body
        msg.attach_alternative(body, 'text/html')
        return msg.send()


class Configuration(models.Model):

    process = models.CharField(
        verbose_name=_("Process"), max_length=200,
        help_text=_("A name to identify the process."))

    mail_template = models.ForeignKey(
        MailTemplate, verbose_name=_("Mail template"),
        on_delete=models.SET_NULL, null=True, blank=True,
        help_text=_("The mail template linked with this configuration "
                    "(process). When required a mail template to this "
                    "configurations this mail template will be returned."))

    description = models.TextField(
        verbose_name=_("Description"), blank=True, null=True,
        help_text=_("Description for configuration. This description can "
                    "contain the contextual variables that are expected to "
                    "be used in associated MailTemplates."))

    class Meta:
        verbose_name = _('Configuration')
        verbose_name_plural = _('Configurations')

    def __str__(self):
        str_ = '{} - '.format(self.process)
        if self.mail_template:
            str_ += str(self.mail_template)
        else:
            str_ += gettext('No mail template')
        return str_

    @staticmethod
    def get_mail_template(process):
        try:
            return Configuration.objects.get(process=process).mail_template
        except ObjectDoesNotExist:
            return None
