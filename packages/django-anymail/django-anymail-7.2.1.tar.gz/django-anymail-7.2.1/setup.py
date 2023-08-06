import re
from codecs import open  # to use a consistent encoding
from collections import OrderedDict
from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

# get versions from anymail/_version.py,
# but without importing from anymail (which would break setup)
with open(path.join(here, "anymail/_version.py"), encoding='utf-8') as f:
    code = compile(f.read(), "anymail/_version.py", 'exec')
    _version = {}
    exec(code, _version)
    version = _version["__version__"]  # X.Y or X.Y.Z or X.Y.Z.dev1 etc.
    release_tag = "v%s" % version  # vX.Y or vX.Y.Z


def long_description_from_readme(rst):
    # Freeze external links (on PyPI) to refer to this X.Y or X.Y.Z tag.
    # (This relies on tagging releases with 'vX.Y' or 'vX.Y.Z' in GitHub.)
    rst = re.sub(r'(?<=branch=)master'     # Travis build status: branch=master --> branch=vX.Y.Z
                 r'|(?<=/)stable'          # ReadTheDocs links: /stable --> /vX.Y.Z
                 r'|(?<=version=)stable',  # ReadTheDocs badge: version=stable --> version=vX.Y.Z
                 release_tag, rst)  # (?<=...) is "positive lookbehind": must be there, but won't get replaced
    return rst


with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = long_description_from_readme(f.read())


setup(
    name="django-anymail",
    version=version,
    description='Django email integration for Amazon SES, Mailgun, Mailjet, Postmark, '
                'SendGrid, SendinBlue, SparkPost and other transactional ESPs',
    keywords="Django, email, email backend, ESP, transactional mail, "
             "Amazon SES, Mailgun, Mailjet, Mandrill, Postmark, SendinBlue, SendGrid, SparkPost",
    author="Mike Edmunds and Anymail contributors",
    author_email="medmunds@gmail.com",
    url="https://github.com/anymail/django-anymail",
    license="BSD License",
    packages=["anymail"],
    zip_safe=False,
    install_requires=["django>=1.11", "requests>=2.4.3", "six"],
    extras_require={
        # This can be used if particular backends have unique dependencies.
        # For simplicity, requests is included in the base requirements.
        "amazon_ses": ["boto3"],
        "mailgun": [],
        "mailjet": [],
        "mandrill": [],
        "postmark": [],
        "sendgrid": [],
        "sendinblue": [],
        "sparkpost": ["sparkpost"],
    },
    include_package_data=True,
    test_suite="runtests.runtests",
    tests_require=["mock", "boto3", "sparkpost"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: BSD License",
        "Topic :: Communications :: Email",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Environment :: Web Environment",
    ],
    long_description=long_description,
    project_urls=OrderedDict([
        ("Documentation", "https://anymail.readthedocs.io/en/%s/" % release_tag),
        ("Source", "https://github.com/anymail/django-anymail"),
        ("Changelog", "https://anymail.readthedocs.io/en/%s/changelog/" % release_tag),
        ("Tracker", "https://github.com/anymail/django-anymail/issues"),
    ]),
)
