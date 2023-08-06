# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['flask_sqlalchemy_pgevents']
install_requires = \
['attr>=0.3.1,<0.4.0',
 'flask-sqlalchemy>=2.4.4,<3.0.0',
 'flask>=1.1.2,<2.0.0',
 'github-webhook>=1.0.2,<2.0.0',
 'psycopg2-binary>=2.8.5,<3.0.0',
 'psycopg2-pgevents>=0.2.1,<0.3.0']

setup_kwargs = {
    'name': 'flask-sqlalchemy-pgevents',
    'version': '0.3.0',
    'description': 'Flask extension for psycopg2-pgevents, using SQLAlchemy.',
    'long_description': "#########################\nflask-sqlalchemy-pgevents\n#########################\n\n.. image:: https://badge.fury.io/py/flask-sqlalchemy-pgevents.svg\n    :target: https://badge.fury.io/py/flask-sqlalchemy-pgevents\n.. image:: https://coveralls.io/repos/github/shawalli/flask-sqlalchemy-pgevents/badge.svg?branch=master\n    :target: https://coveralls.io/github/shawalli/flask-sqlalchemy-pgevents?branch=master\n.. image:: https://img.shields.io/badge/License-MIT-yellow.svg\n    :target: https://opensource.org/licenses/MIT\n\nflask-sqlalchemy-pgevents provides PostGreSQL eventing for Flask. It handles\nsetting up the underlying database, registering triggers, and polling for\nevents.\n\n**************\nWhy Do I Care?\n**************\n\n   *I have SQLAlchemy, which supports event listeners. Why do I care about this\n   extension?*\n\nSQLAlchemy's event listening framework is great for listening to database\nchanges made through SQLAlchemy. However, in the real world, not every data\nevent that affects a database takes place through SQLAlchemy; an application\nmay be created from any number of packages, libraries, and modules written\nin different languages and with different frameworks. If any of these\nnon-SQLAlchemy items modify a database, SQLAlchemy will not know, and will\ntherefore not notify event listeners of these changes.\n\nWith this extension, an application may be notified of events at the\n*database layer*. This means that any changes made to a table are caught by\nthis extension and registered event listeners (for the affected table) are\ncalled.\n\n*******************\nWhy Use SQLAlchemy?\n*******************\n\n    *You just said that SQLAlchemy has nothing to do with the eventing aspect\n    of this extension...So why are you using SQLAlchemy?*\n\nGreat question! SQLAlchemy is primarily used as a convenience mechanism for\ncreating a consistent connection to the database.\n\nAdditionally, many Flask applications use SQLAlchemy as their ORM. As such,\nthis extension will integrate seamlessly with any Flask applications that\nuse `Flask-SQLAlchemy <https://github.com/mitsuhiko/flask-sqlalchemy>`_. To\nprovide a consistent SQLAlchemy experience, this extension's event listener\ndecorator is designed to closely resemble SQLAlchemy event listener decorators.\n\nNote\n    While this extension may appear to integrate with SQLAlchemy's event\n    listeners, it actually sits alongside that eventing structure. Registering\n    a PGEvents event listener does not register the event listener with\n    SQLAlchemy's ``event`` registrar.\n\n********\nExamples\n********\n\nSee the ``examples`` directory for example use cases for this package.\n\n************\nFuture Plans\n************\n\n* With a little bit of work, it should be possible to completely integrate this\n  extension's event listeners into ``SQLAlchemy.event``, so that event listeners\n  are functionally identical to SQLAlchemy's event listeners.\n\n* Currently, the only supported events are after-insert and after-update.\n  The ``psycopg2-pgevent`` package could be updated in coordination with this\n  extension to support other `SQLAlchemy mapper events\n  <http://docs.sqlalchemy.org/en/latest/orm/events.html#mapper-events>`_.\n\n**********\nReferences\n**********\n\n* `psycopg2-pgevents <https://github.com/shawalli/psycopg2-pgevents>`_\n\n* `SQLAlchemy <https://bitbucket.org/zzzeek/sqlalchemy>`_\n\n* `Flask-SQLAlchemy <https://github.com/mitsuhiko/flask-sqlalchemy>`_\n\n**********************\nAuthorship and License\n**********************\n\nWritten by Shawn Wallis and distributed under the MIT license.\n",
    'author': 'Shawn Wallis',
    'author_email': 'shawn.p.wallis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shawalli/flask-sqlalchemy-pgevents',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
