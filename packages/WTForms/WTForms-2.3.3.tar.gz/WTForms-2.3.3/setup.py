import io
import re
from setuptools import setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('wtforms/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='WTForms',
    version=version,
    url='https://wtforms.readthedocs.io/',
    project_urls={
        'Documentation': 'https://wtforms.readthedocs.io/',
        'Code': 'https://github.com/wtforms/wtforms',
        'Issue Tracker': 'https://github.com/wtforms/wtforms/issues',
    },
    license='BSD-3-Clause',
    maintainer='WTForms',
    maintainer_email='davidism@gmail.com',
    description=(
        'A flexible forms validation and rendering library for Python'
        ' web development.'
    ),
    long_description=readme,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=[
        'wtforms',
        'wtforms.csrf',
        'wtforms.fields',
        'wtforms.widgets',
        'wtforms.ext',
        'wtforms.ext.appengine',
        'wtforms.ext.csrf',
        'wtforms.ext.dateutil',
        'wtforms.ext.django',
        'wtforms.ext.django.templatetags',
        'wtforms.ext.i18n',
        'wtforms.ext.sqlalchemy',
    ],
    include_package_data=True,
    install_requires=["MarkupSafe"],
    extras_require={
        "ipaddress": ['ipaddress;python_version<"3.3"'],
        "email": ["email_validator"],
        'locale': ['Babel>=1.3'],
    },
)
