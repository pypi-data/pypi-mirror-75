# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtail_airtable',
 'wagtail_airtable.management.commands',
 'wagtail_airtable.migrations',
 'wagtail_airtable.templatetags']

package_data = \
{'': ['*'],
 'wagtail_airtable': ['templates/wagtail_airtable/*',
                      'templates/wagtailsnippets/snippets/*']}

install_requires = \
['airtable-python-wrapper>=0.13.0,<0.14.0',
 'djangorestframework>=3.11.0,<3.12.0',
 'wagtail>=2.6']

setup_kwargs = {
    'name': 'wagtail-airtable',
    'version': '0.1.3',
    'description': 'Sync data between Wagtail and Airtable',
    'long_description': "Wagtail/Airtable\n================\n\nAn extension for Wagtail allowing content to be transferred between Airtable sheets and your Wagtail/Django models.\n\nDeveloped by `Torchbox <https://torchbox.com/>`_ and sponsored by `The Motley Fool <https://www.fool.com/>`_.\n\n.. image:: https://raw.githubusercontent.com/wagtail/wagtail-airtable/master/examples/preview.gif\n\n`View the repo README for more details <https://github.com/wagtail/wagtail-airtable/>`_\n\n****************************\nInstallation & Configuration\n****************************\n\n* Install the package with ``pip install wagtail-airtable``\n* Add ``'wagtail_airtable'`` to your project's ``INSTALLED_APPS``\n* In your settings you will need to map models to Airtable settings. Every model you want to map to an Airtable sheet will need:\n    * An ``AIRTABLE_BASE_KEY``. You can find the base key in your Airtable docs when you're signed in to Airtable.com\n    * An ``AIRTABLE_TABLE_NAME`` to determine which table to connect to.\n    * An ``AIRTABLE_UNIQUE_IDENTIFIER``. This can either be a string or a dictionary mapping the Airtable column name to your unique field in your model.\n        * ie. ``AIRTABLE_UNIQUE_IDENTIFIER: 'slug',`` this will match the ``slug`` field on your model with the ``slug`` column name in Airtable. Use this option if your model field and your Airtable column name are identical.\n        * ie. ``AIRTABLE_UNIQUE_IDENTIFIER: {'Airtable Column Name': 'model_field_name'},`` this will map the ``Airtable Column Name`` to a model field called ``model_field_name``. Use this option if your Airtable column name and your model field name are different.\n    * An ``AIRTABLE_SERIALIZER`` that takes a string path to your serializer. This helps map incoming data from Airtable to your model fields. Django Rest Framework is required for this. See the [examples/](examples/) directory for serializer examples.\n\n* Lastly make sure you enable wagtail-airtable with ``WAGTAIL_AIRTABLE_ENABLED = True``. By default this is disabled so data in your Wagtail site and your Airtable sheets aren't accidentally overwritten. Data is hard to recover, this option helps prevent accidental data loss.\n\n**************************\nExample Base Configuration\n**************************\n\nBelow is a base configuration or ``ModelName`` and ``OtherModelName`` (both are registered Wagtail snippets), along with ``HomePage``.\n\n.. code-block:: python\n\n    # your settings.py\n    AIRTABLE_API_KEY = 'yourSuperSecretKey'\n    WAGTAIL_AIRTABLE_ENABLED = True\n    AIRTABLE_IMPORT_SETTINGS = {\n        'appname.ModelName': {\n            'AIRTABLE_BASE_KEY': 'app3ds912jFam032S',\n            'AIRTABLE_TABLE_NAME': 'Your Airtable Table Name',\n            'AIRTABLE_UNIQUE_IDENTIFIER': 'slug', # Must match the Airtable Column name\n            'AIRTABLE_SERIALIZER': 'path.to.your.model.serializer.CustomModelSerializer'\n        },\n        'appname.OtherModelName': {\n            'AIRTABLE_BASE_KEY': 'app4ds902jFam035S',\n            'AIRTABLE_TABLE_NAME': 'Your Airtable Table Name',\n            'AIRTABLE_UNIQUE_IDENTIFIER':\n                'Page Slug': 'slug', # 'Page Slug' column name in Airtable, 'slug' field name in Wagtail.\n            },\n            'AIRTABLE_SERIALIZER': 'path.to.your.model.serializer.OtherCustomModelSerializer'\n        },\n        'pages.HomePage': {\n            'AIRTABLE_BASE_KEY': 'app2ds123jP23035Z',\n            'AIRTABLE_TABLE_NAME': 'Wagtail Page Tracking Table',\n            'AIRTABLE_UNIQUE_IDENTIFIER':\n                'Wagtail Page ID': 'pk',\n            },\n            'AIRTABLE_SERIALIZER': 'path.to.your.pages.serializer.PageSerializer',\n            # Below are OPTIONAL settings.\n            # By disabling `AIRTABLE_IMPORT_ALLOWED` you can prevent Airtable imports\n            # Use cases may be:\n            #   - disabling page imports since they are difficult to setup and maintain,\n            #   - one-way sync to Airtable only (ie. when a model/Page is saved)\n            # Default is True\n            'AIRTABLE_IMPORT_ALLOWED': False,\n            # Add the AIRTABLE_BASE_URL setting if you would like to provide a nice link\n            # to the Airtable Record after a snippet or Page has been saved.\n            # To get this URL open your Airtable base on Airtable.com and paste the link.\n            # The recordId will be automatically added so please don't add that\n            # You can add the below setting. This is optional and disabled by default.\n            'AIRTABLE_BASE_URL': 'https://airtable.com/tblxXxXxXxXxXxXx/viwxXxXxXxXxXxXx',\n        },\n        # ...\n    }\n\n`View the repo README for more details <https://github.com/wagtail/wagtail-airtable/>`_\n",
    'author': 'Kalob Taulien',
    'author_email': 'kalob.taulien@torchbox.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wagtail/wagtail-airtable',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<=3.8',
}


setup(**setup_kwargs)
