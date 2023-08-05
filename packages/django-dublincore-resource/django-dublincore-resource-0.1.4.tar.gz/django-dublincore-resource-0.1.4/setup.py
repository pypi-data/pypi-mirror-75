# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dublincore_resource', 'dublincore_resource.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django-controlled-vocabulary<2', 'django>=2.2,<3.0']

setup_kwargs = {
    'name': 'django-dublincore-resource',
    'version': '0.1.4',
    'description': 'Describe your resources with a Dublin Core schema',
    'long_description': '# Django Dublin Core Resource\n\nA Django model and admin interface to manage metadata about your resources\nusing [standard Dublin Core (DC) schema](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/).\n\nThe approach taken by this app is to centralise all your resource metadata\ninto a single table.\n\n<p align="center">\n  <img src="docs/img/resource-change-1.png" height="400">\n</p>\n\n# Data Models\n\n* AbstractDublinCoreResource\n  * an abstract Django Model that replicate the Dublin Core schema\n  * each [DC element](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3) (dc:) is represented by a field\n  * some [DC terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-2) (dcterms:) are also included\n  * makes use of ControlledTermField for links to controlled vocabularies\n* DublinCoreResource\n  * inherit from AbstractDublinCoreResource\n* DublinCoreAgent\n  * represents a person or organisation\n* DublinCoreRights\n  * represents Rights statements that can be shared among your resources\n\n# Features\n\n* One centralised table for all your resource\n* Standard Dublin Core elements/fields\n* Lookup values into authority lists / controlled vocabularies\n* Inline description of all fields\n* Extensible model\n* [TODO] optional integration with Wagtail Image gallery and Documents\n* [TODO] smart bulk import/update from CSV\n* [TODO] advanced input validations\n* [TODO] API / export into various standard formats\n* [TODO] support for file attachment / upload\n* [TODO] support for bibliographic citation parsing / extraction\n* [TODO] support for [EDTF dates](https://pypi.org/project/edtf/)\n* [TODO] use Creative Commons [best practices](https://wiki.creativecommons.org/wiki/Best_practices_for_attribution) and [schema](https://creativecommons.org/ns#) for the rights\n\n# Set up\n\n## Installation\n\nFirst [install django-controlled-vocabulary](https://github.com/kingsdigitallab/django-controlled-vocabulary#setup).\n\nThen install the django-dublincore-resource app:\n\n```\npip install django-dublincore-resource\n```\n\nAdd the app to the INSTALLED_APPS list in your Django settings.py file:\n\n```\nINSTALLED_APPS = [\n    ...\n    \'dublincore_resource\',\n    ...\n]\n```\n\nRun the schema migrations:\n\n```\n./manage.py migrate\n```\n\n## Configuration\n\nThe following settings vars are defined by default but can be overridden\nin your Django settings.py.\n\nBy default this app provides a DublinCoreResource model that inherit\nfrom the abstract AbstractDublinCoreResource model. Set the following to\nFalse to define your own model.\n\n```\n# Set to True to disable the DublinCoreResource model and define your own\nDUBLINCORE_RESOURCE_ABSTRACT_ONLY = False\n```\n\n```\n# The path where resource file are uploaded, relative to your MEDIA path\nDUBLINCORE_RESOURCE_UPLOAD_PATH = \'uploads/dublin_core/\'\n```\n',
    'author': 'geoffroy-noel-ddh',
    'author_email': 'geoffroy.noel@kcl.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kingsdigitallab/django-dublincore-resource',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
