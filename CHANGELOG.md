# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [2.4.0] - 2019-01-10

### Added
- Django 2.2 support

## [2.3.0] - 2019-01-10

### Added
- Allow optional setting `ONELOGIN_IDP_ENTITY_ID`, which provides a custom entity id in the IDP's metadata URL, instead of the connector id

## [2.2.0] - 2018-12-07

### Added
- Django 2.1 support

## [2.1.1] - 2018-02-28

### Changed
- Require [python3-saml](https://github.com/onelogin/python3-saml) >= 1.4.0 (fixes [CVE-2017-11427](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-11427))

## [2.1.0] - 2018-02-22

### Added
- Python 3.6 support
- Django 2.0 support

## [2.0.0] - 2018-01-30

### Added
- Simplified setup in Django projects using OneLogin as an identity provider
- Django 1.10-1.11 support
- Miscellaneous repo quality improvements:
  - Added initial tests
  - Run tests on Travis-CI and monitor code coverage using CodeCov
  - Added .gitignore
  - Fixed various linting errors
  - Added LICENSE file to the root of the project

### Changed
- FIX: Update user attributes on sign-in, instead of just on user creation
- FIX: Allow names to be optional in the SAML Response

### Removed
- Django 1.4-1.7 support
