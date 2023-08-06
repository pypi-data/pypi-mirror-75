# Change Log
## [v0.1.11] - 2020-07-30

### Added

- Add translation files not included in previous releases now: english and 
 spanish.

## [v0.1.10] - 2020-07-30

### Changed

- Fix code quality with migration file.

- Add translation to Configuration model.

## [v0.1.9] - 2020-07-27

### Changed

- Body field restriction on maximum number of characters is removed.

## [v0.1.8] - 2020-07-21

### Added

- Add elements for translation.

- Add content to LICENSE file.

## [v0.1.7] - 2020-07-21

### Added

- Travis CI Configuration

### Changed

- README.md is updated for publication

- Remove comments from models files.

## [v0.1.6] - 2020-07-15

### Added

- Add an action in admin site for MailTemplate that let to test selected
 MailTemplates. It requires each MailTemplate to be tested to have a valid
 value in To field temporally, if not the send test will fail.

## [v0.1.5] - 2020-07-13

### Added

- Add cc, bcc, reply_to fields to MailTemplate model.

- Add more translations.

### Changed

- Now MailTemplate use EmailMultiAlternatives class for creating and sending
 mails.

- MailTemplate body field is added to EmailMultiAlternatives instance as
 body, and also attached as alternative as "text/html"


## [v0.1.4] - 2020-07-12

### Added

- Add Description field to Configuration model.

- Add Description field to MailTemplate model.

- Add Title field to MailTemplate model.

- More elements for translation.

### Changed

- Modify string representation of MailTemplate model. Each MailTemplate now is
 represented by it's title.  

## [v0.1.3] - 2020-05-05

### Added

- New advanced section in documentation.

### Changed


## [v0.1.2] - 2020-01-14

### Added

- More elements for translation.

- Add verbose name (and tests) to models so they can be translated.

### Changed

- replace_context_variable function follow [documentation example](https://docs.python.org/3/library/stdtypes.html#str.format_map)
 using ``string.format_map`` instead of ``string.format`` and define Default
 dict type for returning missing key value. 

## [v0.1.1] - 2020-01-11

### Added

- Migrations files.

- This change log file.

- Spanish locale translation.

### Changed

- MailTemplate's body field change type from CharField to TextField.

- Documentation review.


## [v0.1.0] - 2020-01-09
First beta version. 

All test and initial models.
