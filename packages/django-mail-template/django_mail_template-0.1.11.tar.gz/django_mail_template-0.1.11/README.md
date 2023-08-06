![Django roles access](https://django-mail-template.github.io/_images/django-mail-template.png "Django mail template")  
# Django Mail Template
![](https://img.shields.io/badge/release-v0.1.7-blue.svg)
![](https://img.shields.io/badge/state-production-brightgreen.svg)
[![Build Status](https://travis-ci.org/Django-Mail-Template/master.svg?branch=master)](https://travis-ci.org/Django-Mail-Template/master)
[![codecov](https://codecov.io/gh/django-mail-template/master/branch/master/graph/badge.svg)](https://codecov.io/gh/django-mail-template/master)


A very simple Django application for:

* Provide *basic template* features for mails subjects and bodies.

* Provide needed infrastructure to let administrative users create/edit mails
  used by applications.
  
## Description

``django_mail_template`` is a very simple application to create mails templates
with context variables, and then send mails with context variables replaced
with values. Mails templates are created with *Django admin interface*.

For example, if context variables are: *first_name* and *last_name*, while
cycling a collection of people (clients, providers, and like) is possible to
send a mail to each of them using their first name and last name to replace
the context variables in *MailTemplate* body or subject:

``Dear {first_name} {last_name} have a great new year!!!``

Also with indirect use between *MailTemplate* and *Configuration* is
possible to change at run time the mail template mapped to a piece of code
through a *Configuration* instance. 

For example, create two mail template: one with christmas greeting text
and subject, and other mail template with new year greeting text and subject.
Then the same process (code) used in upper example can be used to send
christmas and new year greeting to all people. 

Change which mail template is used by which process in *Django admin
interface*.

#### Works with:

* Django 1.11+ (Python 3.5+)

* Django 2+ (Python 3.5+)

* Django 3+ (Python 3.5+)

* [Documentation](https://django-mail-template.github.io)


## Requirements

1) Django's email docs specify all requirements for sending mail with
django.core.mail (
[Django email](https://docs.djangoproject.com/en/dev/topics/email/)).

2) ``django_mail_template`` uses *Django admin site*, check official
documentation for it's requirements:
[Django admin site](https://docs.djangoproject.com/en/dev/ref/contrib/admin/).

3) ``django_mail_template`` uses 
[Django CKEditor](https://github.com/django-ckeditor/django-ckeditor) to let write rich text
MailTeamplate.


## Quick start


### Installation and configuration


1. Install `django_mail_template` from pypi:
```
    pip install django-mail-template
```

2. Add `'django_mail_template'` and `'ckeditor'` to your `INSTALLED_APPS` setting:
```    
    INSTALLED_APPS = [
        ...
        'ckeditor'
        'django_mail_template',
    ]
```
    
3. Run migrations to create **django_mail_template** models:
```
    python manage.py migrate
```

4. Run the collectstatic management command:
```
    python manage.py collectstatic
```

### Use Django Mail Template

#### 1. Direct use
You can simple use ``django_mail_template`` to send mails:
```
    from django_mail_template.models import MailTemplate

    mail_template = MailTemplate(title="A mail Title", from="a@b.com",
                                 to="b@b.com",
                                 subject="Django Mail Template quick start.")
    mail_template.send()
```

#### 2. Template features
``django_mail_template``'s *basic template* feature is based in variables
replacement with Python string format:
```
    from django_mail_template.models import MailTemplate

    ...
    mail_template = MailTemplate.create(
        title="First mail template",
        from="a@b.com",
        subject="Hello {client}.",
        body="Dear {client}: We are delivering your {product}."
    )

    ...
    mail_template.to = ["bobtheclient@c.com"]
    mail_template.send({"client": "Bob TheClient",
                        "product": "Great product"})
```

Administrative users can create or edit ``MailTemplate`` using *Django admin
site* and redact text using Python string format.

#### 3. Indirect use
Is also possible to use an indirect call through ``Configuration`` data model.
In *Django admin site* (or by code) you can create:
```
    a_mail_template_greeting = MailTemplate.objects.create(
        title="First mail template",
        from="a@b.com",
        subject="Hello {client}.",
        body="Dear {client}: We wish you {greeting}.")

    configuration = Configuration.objects.create(
        process="clients_greeting",
        mail_template=a_mail_template_greeting
    )
```

Then in code

```
    from django_mail_template.models import Configuration

    mail_template = Configuration.get_mail_template("clients_greeting")
    # Cycle through clients
        mail_template.to = client.email
        mail_template.send({"client": client.name,
                            "greeting": "A great mew year!!!"})
```


#### 4. Django admin interface

When ``django_mail_template`` is installed, and migrations applied, *Django
admin site* will expose to administrative users a new section with title
*Django Mail Template*. User can manage ``MailTempaltes`` and 
``Configurations`` from there:

* ``MailTemplate``: Users can redact mails (create, edit, delete).

* ``Configuration``: If code points to *Configurations* (indirect use),
  administrative users can change mapped *MailTemplate* to use new mail
  template without changing code.

* Test created *mail templates*


## More about Django mail template

You can check the **django_mail_template** test execution at 
[Travis CI integration](https://travis-ci.org/django-mail-template/master)
([![Build Status](https://travis-ci.org/django-mail-template/master.svg?branch=master)](https://travis-ci.org/django-mail-template/master))

You can also check **django_mail_template** test coverage at
[Coverage](https://django-mail-template.github.io/coverage.html)
([![codecov](https://codecov.io/gh/django-mail-template/master/branch/master/graph/badge.svg)](https://codecov.io/gh/django-mail-template/master))


## Related sites

* [Documentation](https://django-mail-template.github.io)

* [Package at pypi.org](https://pypi.org/project/django-mail-template/)

* [source code](https://github.com/django-mail-template/master)

* [Travis CI integration](https://travis-ci.org/django-mail-template/master)

* [Codecov](https://codecov.io/gh/django-mail-template/master)

