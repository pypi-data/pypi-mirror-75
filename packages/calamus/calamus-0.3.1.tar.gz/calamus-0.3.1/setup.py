# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calamus']

package_data = \
{'': ['*']}

install_requires = \
['lazy-object-proxy>=1.4.3,<2.0.0',
 'marshmallow>=3.5.1,<4.0.0',
 'pyld>=2.0.2,<3.0.0']

extras_require = \
{'docs': ['sphinx>=3.0.3,<4.0.0',
          'sphinx-rtd-theme>=0.4.3,<0.5.0',
          'sphinxcontrib-spelling>=5.0.0,<6.0.0']}

setup_kwargs = {
    'name': 'calamus',
    'version': '0.3.1',
    'description': 'calamus is a library built on top of marshmallow to allow (de-)Serialization of Python classes to JSON-LD.',
    'long_description': '..\n    Copyright 2017-2020 - Swiss Data Science Center (SDSC)\n    A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and\n    Eidgenössische Technische Hochschule Zürich (ETHZ).\n\n    Licensed under the Apache License, Version 2.0 (the "License");\n    you may not use this file except in compliance with the License.\n    You may obtain a copy of the License at\n\n        http://www.apache.org/licenses/LICENSE-2.0\n\n    Unless required by applicable law or agreed to in writing, software\n    distributed under the License is distributed on an "AS IS" BASIS,\n    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n    See the License for the specific language governing permissions and\n    limitations under the License.\n\n.. image:: https://github.com/SwissDataScienceCenter/calamus/blob/master/docs/reed.png?raw=true\n   :align: center\n\n==================================================\n calamus: JSON-LD Serialization Library for Python\n==================================================\n\n.. image:: https://readthedocs.org/projects/calamus/badge/?version=latest\n   :target: https://calamus.readthedocs.io/en/latest/en/latest/?badge=latest\n   :alt: Documentation Status\n\n.. image:: https://github.com/SwissDataScienceCenter/calamus/workflows/Test,%20Integration%20Tests%20and%20Deploy/badge.svg\n   :target: https://github.com/SwissDataScienceCenter/calamus/actions?query=workflow%3A%22Test%2C+Integration+Tests+and+Deploy%22+branch%3Amaster\n\n.. image:: https://badges.gitter.im/SwissDataScienceCenter/calamus.svg\n   :target: https://gitter.im/SwissDataScienceCenter/calamus?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge\n\ncalamus is a library built on top of marshmallow to allow (de-)Serialization\nof Python classes to JSON-LD\n\n\nInstallation\n============\n\ncalamus releases and development versions are available from `PyPI\n<https://pypi.org/project/calamus/>`_. You can install it using any tool that\nknows how to handle PyPI packages.\n\nWith pip:\n\n::\n\n    $ pip install calamus\n\n\nUsage\n=====\n\nAssuming you have a class like\n\n::\n\n    class Book:\n        def __init__(self, _id, name):\n            self._id = _id\n            self.name = name\n\nDeclare schemes\n---------------\nYou can declare a schema for serialization like\n::\n\n    schema = fields.Namespace("http://schema.org/")\n\n    class BookSchema(JsonLDSchema):\n        _id = fields.Id()\n        name = fields.String(schema.name)\n\n        class Meta:\n            rdf_type = schema.Book\n            model = Book\n\nThe ``fields.Namespace`` class represents an ontology namespace.\n\nMake sure to set ``rdf_type`` to the RDF triple type you want get and\n``model`` to the python class this schema applies to.\n\nSerializing objects ("Dumping")\n-------------------------------\n\nYou can now easily serialize python classes to JSON-LD\n\n::\n\n    book = Book(_id="http://example.com/books/1", name="Ilias")\n    jsonld_dict = BookSchema().dump(book)\n    #{\n    #    "@id": "http://example.com/books/1",\n    #    "@type": "http://schema.org/Book",\n    #    "http://schema.org/name": "Ilias",\n    #}\n\n    jsonld_string = BookSchema().dumps(book)\n    #\'{"@id": "http://example.com/books/1", "http://schema.org/name": "Ilias", "@type": "http://schema.org/Book"}\')\n\nDeserializing objects ("Loading")\n---------------------------------\n\nYou can also easily deserialize JSON-LD to python objects\n\n::\n\n    data = {\n        "@id": "http://example.com/books/1",\n        "@type": "http://schema.org/Book",\n        "http://schema.org/name": "Ilias",\n    }\n    book = BookSchema().load(data)\n    #<Book(_id="http://example.com/books/1", name="Ilias")>\n\n\nSupport\n=======\n\nYou can reach us on our `Gitter Channel <https://gitter.im/SwissDataScienceCenter/calamus>`_.\n',
    'author': 'Swiss Data Science Center',
    'author_email': 'contact@datascience.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SwissDataScienceCenter/calamus/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
