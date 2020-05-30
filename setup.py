"""Installation script for flask-qldb-boilerplate application."""
import os
import re
from pathlib import Path

from setuptools import setup, find_packages

DESCRIPTION = (
    "Boilerplate Flask API for AWS QLDB with Flask-RESTx, SQLAlchemy, boto3, amazon.ion, "
    "pytest-dotenv configured"
)
APP_ROOT = Path(__file__).parent
README = (APP_ROOT / "README.md").read_text()
AUTHOR = "Sajib Hassan"
AUTHOR_EMAIL = "sajib.hassan@gmail.com"
PROJECT_URLS = {
    "Documentation": "https://aaronluna.dev/series/flask-api-tutorial/",
    "Bug Tracker": "https://github.com/a-luna/flask-api-tutorial/issues",
    "Source Code": "https://github.com/a-luna/flask-api-tutorial",
}
INSTALL_REQUIRES = [
    "alembic==1.4.2",
    "aniso8601==8.0.0",
    "attrs==19.3.0",
    "bcrypt==3.1.7",
    "cffi==1.14.0",
    "click==7.1.2",
    "Flask==1.1.2",
    "Flask-Bcrypt==0.7.1",
    "Flask-Migrate==2.5.3",
    "flask-restx==0.2.0",
    "Flask-Script==2.0.6",
    "Flask-SQLAlchemy==2.4.1",
    "Flask-Testing==0.8.0",
    "importlib-metadata==1.6.0",
    "itsdangerous==1.1.0",
    "Jinja2==2.11.2",
    "jsonschema==3.2.0",
    "Mako==1.1.2",
    "MarkupSafe==1.1.1",
    "pycparser==2.20",
    "PyJWT==1.7.1",
    "pyrsistent==0.16.0",
    "python-dateutil==2.8.1",
    "python-editor==1.0.4",
    "pytz==2020.1",
    "six==1.14.0",
    "SQLAlchemy==1.3.17",
    "Werkzeug==0.16.1",
    "zipp==3.1.0",
    'amazon.ion>=0.5.0,<0.6',
    'boto3>=1.9.237,<2',
    'botocore>=1.12.237,<2',
    'pyqldb>=2.0.0,<3'
]
EXTRAS_REQUIRE = {
    "dev": [
        "pytest-dotenv",
    ]
}

ROOT = os.path.join(os.path.dirname(__file__), 'hash_chain')
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.a-z\-]+)['"]''')


def get_version():
    init = open(os.path.join(ROOT, '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


try:
    os.makedirs(os.path.join(ROOT, 'instance'))
except OSError:
    pass

setup(
    name="flask-qldb-boilerplate",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    version=get_version(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    license="MIT",
    url="https://github.com/a-luna/flask-api-tutorial",
    project_urls=PROJECT_URLS,
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
)
