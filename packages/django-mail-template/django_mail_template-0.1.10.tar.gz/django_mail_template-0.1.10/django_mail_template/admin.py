# -*- coding: UTF-8 -*-
from django.contrib import admin, messages
from django.utils.translation import gettext as _

from django_mail_template.models import MailTemplate, Configuration


class MailTemplateAdmin(admin.ModelAdmin):

    actions = ['test_mail_template']

    def test_mail_template(self, request, queryset):
        send_mail = 0
        for mail_template in queryset:
            if mail_template.to is None or mail_template.to == '':
                err_msg = _('MailTemplate {}: Do not have a email '
                            'address in To Field').format(mail_template.title)
                self.message_user(request, err_msg, messages.ERROR)
            else:
                try:
                    # send with context={} is to force replacement and detect
                    # any error
                    mail_template.send(context={})
                    send_mail += 1
                except ValueError as e:
                    err_msg = _('MailTemplate {}: Gives an error when '
                                'trying to send it. Most likely: please check '
                                'subject and body uses context variables as '
                                'expected: "{{variable{{" and "}}variable}}" '
                                'are both wrong use. The error detail: {} '
                                '({}).').format(mail_template.title, str(e),
                                                type(e))
                    self.message_user(request, err_msg, messages.ERROR)
                except Exception as e:
                    # Catch any exception as it is a test.
                    err_msg = _('MailTemplate {}: Gives an error when '
                                'trying to send it: {} ({}).').format(
                                 mail_template.title, str(e), type(e))
                    self.message_user(request, err_msg, messages.ERROR)
        if send_mail > 0:
            msg = _('Amount of sent mails: {}.').format(send_mail)
            self.message_user(request, msg, messages.SUCCESS)

    test_mail_template.short_description = _('Test mails templates')


admin.site.register(MailTemplate, MailTemplateAdmin)
admin.site.register(Configuration)
