# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added
- Python 3.6 support

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
