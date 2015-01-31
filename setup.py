from setuptools import setup, find_packages
from saml_service_provider import __version__ as version

setup(
    name='django-saml-service-provider',
    version=version,
    description='',
    long_description='',
    author='Kristian Oellegaard',
    author_email='kristian@kristian.io',
    url='https://github.com/KristianOellegaard/django-saml-service-provider',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Django>=1.4',
        'python-saml'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
    ]
)