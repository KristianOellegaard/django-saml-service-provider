from setuptools import Command, find_packages, setup

from saml_service_provider import __version__ as version


class TestCommand(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import django
        from django.conf import settings
        from django.core.management import call_command

        settings.configure(
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3',
                },
            },
            INSTALLED_APPS=(
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
            ),
            MIDDLEWARE=('django.contrib.sessions.middleware.SessionMiddleware',),
            MIDDLEWARE_CLASSES=('django.contrib.sessions.middleware.SessionMiddleware',),  # Django < 1.10
            ROOT_URLCONF='saml_service_provider.urls',
            AUTHENTICATION_BACKENDS=['saml_service_provider.auth_backend.SAMLServiceProviderBackend']
        )
        django.setup()
        call_command('test', 'saml_service_provider')


setup(
    name='django-saml-service-provider',
    version=version,
    license='BSD License',
    description='Easily let users sign in via SAML 2.0 to your django app.',
    long_description='',
    author='Kristian Oellegaard',
    author_email='kristian@kristian.io',
    url='https://github.com/KristianOellegaard/django-saml-service-provider',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Django >= 1.8, < 3.0',
        'python3-saml >= 1.4.0',
    ],
    tests_require=[
        'mock',
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        "Framework :: Django :: 1.10",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
    ],
    cmdclass={'test': TestCommand}
)
