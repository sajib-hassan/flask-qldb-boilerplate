Flask API wrapper of AWS QLDB - RESTx Boilerplate
=================================================

The goals that were achived in this boilerplate:

* RESTx API server should be self-documented using OpenAPI (fka Swagger)
  specifications, so interactive documentation UI is in place;
* Authentication is handled with JWT for first-party clients makes it usable
  not only for third-party "external" apps;
* Permissions are handled (and automaticaly documented);
* Extensive testing with good code coverage.

![Flask RESTx QLDB APIs](https://raw.githubusercontent.com/sajib-hassan/flask-qldb-boilerplate/master/docs/static/hash-chain-apis.png)


Project Structure
-----------------

### Root folder

Folders:

* `hash_chain\app` - This RESTx API wrapper of AWS QLDB implementation is here.
* `hash_chain\tests` - These are [unittest](https://docs.python.org/3/library/unittest.html) tests for this RESTx API 
wrapper of AWS QLDB implementation.
* `migrations` - Database migrations are stored here.

Files:

* `.env.sample` - Application Config for environment variables, you have to copy this file and rename to `.env`.
* `.flaskenv.sample` - Flask Config for environment variables, you have to copy this file and rename to `.flaskenv`.
* `.gitignore` - Lists files and file masks of the files which should not be
  added to git repository.
* `config.py.sample` - This is a config file of this RESTx API wrapper of AWS QLDB implementation. You have to copy 
this file and rename to `config.py`.
* `local_config.py.sample` - The local environment config file that will overwrite `DevelopmentConfig`. You have to copy 
this file and rename to `local_config.py`.
* `Makefile` - This is a configuration file for the `make` command. All `make` command preserved here.
* `manage.py` - This is a ultimate entry-point of this application.
* `LICENSE` - MIT License, i.e. you are free to do whatever is needed with the
  given code with no limits.
* `README.md`
* `requirements.txt` - The list of Python requirements.
* `setup.py` - Project setup file with Python requirements.

### Application Structure

```
hash_chain/
├── __init__.py
├── app/
│   ├── __init__.py
│   ├── extensions
│   │   ├── __init__.py
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   ├── api.py
│   │   │   └── http_exception.py
│   │   ├── app_config
│   │   │   └── __init__.py
│   │   ├── flask_bcrypt
│   │   │   └── __init__.py
│   │   ├── flask_qldb
│   │   │   ├── __init__.py
│   │   │   └── connect_to_ledger.py
│   │   ├── flask_sqlalchemy
│   │   │   └── __init__.py
│   │   └── logging
│   │      └── __init__.py
│   ├── modules
│   │   ├── __init__.py
│   │   ├── api
│   │   │   └── __init__.py
│   │   ├── auth
│   │   │   ├── __init__.py
│   │   │   ├── controllers.py
│   │   │   ├── decorators.py
│   │   │   ├── dto.py
│   │   │   ├── models.py
│   │   │   └── services.py
│   │   ├── users
│   │   │   ├── __init__.py
│   │   │   ├── controllers.py
│   │   │   ├── dto.py
│   │   │   ├── models.py
│   │   │   └── services.py
│   │   └── ledger
│   │       ├── __init__.py
│   │       ├── dto.py
│   │       ├── helpers.py
│   │       ├── core
│   │       ├── ddl
│   │       ├── dml
│   │       └── verifiable   
│   └── util
│       ├── __init__.py      
│       ├── datetime_util.py      
│       ├── exceptions.py      
│       └── result.py      
│
├── test/  
    ├── __init__.py
    └── ......  

```

* `app/__init__.py` - The entrypoint to this RESTx API Server example
  application (Flask application is created here).
* `app/extensions` - All extensions (e.g. SQLAlchemy, flask_qldb, app_config) are initialized
  here and can be used in the application by importing as, for example,
  `from hash_chain.app.extensions import db`.
* `app/modules` - All endpoints are expected to be implemented here in logicaly
  separated modules. It is up to you how to draw the line to separate concerns
* `app/util` - All utility classes and functions here. 


### Module Structure

Once you added a module name into `config.ENABLED_MODULES`, it is required to
have `your_module.init_app(app, **kwargs)` function. Everything else is
completely optional. Thus, here is the required minimum:

```
your_module/
└── __init__.py
```

, where `__init__.py` will look like this:

```python
def init_app(app, **kwargs):
    pass
```

In this example, however, `init_app` imports `controller` and registeres `api`
(an instance of `flask_restx.Namespace`).


Where to start reading the code?
--------------------------------

The easiest way to start the application is by using make command `run`
implemented in [`manage.py`](manage.py):

```
$ make run
```
OR

```
$ python3 manage.py run
```
OR

```
$ flask run
```

The command creates an application by running
[`hash_chain/app/__init__.py:create_app()`](hash_chain/app/__init__.py) function, which in its turn:

1. loads an application config;
2. initializes extensions:
   [`hash_chain/app/extensions/__init__.py:init_app()`](hash_chain/app/extensions/__init__.py);
3. initializes modules:
   [`hash_chain/app/modules/__init__.py:init_app()`](hash_chain/app/modules/__init__.py).

Modules initialization calls `init_app()` in every enabled module
(listed in `config.ENABLED_MODULES`).

Let's take `ledger` module as an example to look further.
[`hash_chain/app/modules/ledger/__init__.py:init_app()`](hash_chain/app/modules/teams/__init__.py)
imports and registers `api` instance of `flask_restx.Namespace`
from `.controller`. Flask-RESTx `Namespace` is designed to provide similar
functionality as Flask `Blueprint`.

The ledger modules also initialization calls `init_app()` in every enabled module
(listed in `config.ENABLED_LEDGER_MODULES`) inn the same way as the parent modules.

[`api.route()`](hash_chain/app/modules/ledger/ddl/controller.py) is used to bind a
resource (classes inherited from `flask_restx.Resource`) to a specific
route.

Lastly, every `Resource` should have methods which are lowercased HTTP method
names (i.e. `.get()`, `.post()`, etc). This is where users' requests end up.


Dependencies
------------

### Project Dependencies

* [**Python**](https://www.python.org/) 3.5+
* [**flask-restx**](https://flask-restx.readthedocs.io/en/latest/) (+
  [*flask*](http://flask.pocoo.org/))
* [**sqlalchemy**](http://www.sqlalchemy.org/) (+
  [*flask-sqlalchemy*](http://flask-sqlalchemy.pocoo.org/)) - Database ORM.
* [**sqlalchemy-utils**](https://sqlalchemy-utils.rtdf.org/) - for nice
  custom fields (e.g., `PasswordField`).
* [**alembic**](https://alembic.rtdf.org/) - for DB migrations.
* [**marshmallow**](http://marshmallow.rtfd.org/) (+
  [*marshmallow-sqlalchemy*](http://marshmallow-sqlalchemy.rtfd.org/),
  [*flask-marshmallow*](http://flask-marshmallow.rtfd.org/)) - for
  schema definitions. (*supported by the patched Flask-RESTx*)
* [**bcrypt**](https://github.com/pyca/bcrypt/) - for password hashing (used as
  a backend by *sqlalchemy-utils.PasswordField*).
* [**boto3**](https://github.com/boto/boto3) - AWS SDK for Python.
* [**pyqldb**](https://github.com/awslabs/amazon-qldb-driver-python) - A Python implementation of a driver 
  for Amazon QLDB.
* [**amazon.ion**](https://github.com/amzn/ion-python) - A Python implementation of Amazon Ion.
* [**Swagger-UI**](https://github.com/swagger-api/swagger-ui) - for interactive
  RESTx API documentation.


Installation
------------
### From sources

#### Clone the Project

```bash
$ git clone https://github.com/sajib-hassan/flask-qldb-boilerplate.git
```

#### Setup Environment

It is recommended to use virtualenv or pipenv to manage Python
dependencies. Please, learn details yourself.

#### Run python packages and DB migration installation
```bash
$ make install
```
OR 

Run the following commands 
```bash
# python-packages:
$ pip3 install -r requirements.txt

# python-setup:
$ pip3 install -e .

# db-init:
$ python3 manage.py db init

# db-migrate:
$ python3 manage.py db migrate --message "${message:='database migration'}"

# db-upgrade:
$ python3 manage.py db upgrade

```

#### Create users
* Admin user email `joe_admin@gmail.com` with password `admin`
* Regular user email `joe@gmail.com` with password `user`

```bash
$ make seed-users
```

#### Run Server

NOTE: All dependencies and database migrations was handled by above command `make install`,
so go ahead and turn the server ON!

```bash
$ make run
```


Quickstart
----------

Open online interactive API documentation:
[http://127.0.0.1:5000/api/v1/](http://127.0.0.1:5000/api/v1/)

Autogenerated swagger config is always available from
[http://127.0.0.1:5000/api/v1/swagger.json](http://127.0.0.1:5000/api/v1/swagger.json)

`instance/hash_chain_dev.db` (SQLite) includes 2 users:

* Admin user email `joe_admin@gmail.com` with password `admin`
* Regular user email `joe@gmail.com` with password `user`

NOTE: Use On/Off switch in documentation to sign in.



### Run the tests

```bash
$ make tests
```

### Using Postman ####

    Authorization header is in the following format:

    Key: Authorization
    Value: "token_generated_during_login"

    For testing authorization, url for getting all user requires an admin token while url for getting a single
    user by public_id requires just a regular authentication.

### Inspiration from
* [flask-restplus-server-example](https://github.com/frol/flask-restplus-server-example)
* [flask-restplus-boilerplate](https://github.com/cosmic-byte/flask-restplus-boilerplate)
* [exploreflask.com](http://exploreflask.com/en/latest/)

### Contributing
If you want to contribute to this flask QLDB boilerplate, clone the repository and just start making pull requests.

```
https://github.com/sajib-hassan/flask-qldb-boilerplate.git
```

