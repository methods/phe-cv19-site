Methods Wagtail Base
==============

<!-- Build status badges from the chosen pipeline -->

-----------

<!-- vim-markdown-toc GitLab -->

* [About this application](#about-this-application)
    * [Purpose of this app](#purpose-of-this-app)
    * [Tech stack](#tech-stack)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
    * [Without Docker](#without-docker)
    * [With Docker](#with-docker)
  * [Running the database](#running-the-database)
  * [Environment variables](#environment-variables)
  * [Running the site](#running-the-site)
    * [Running without Docker](#running-without-docker)
    * [Running with Docker](#running-with-docker)
      * [Useful  commands](#useful-commands)
      * [Adding new dependencies](#adding-new-dependencies)
* [Contributing](#contributing)
* [License](#license)

<!-- vim-markdown-toc -->


## About this application

### Purpose of this app

The purpose of this app is to provide a project base point for us to deliver CMS projects using Wagtail.

### Tech stack

This application is based on the Wagtail CMS.
It utilises:
- Wagtail CMS
- Python/Django framework
- jQuery
- SASS

## Getting Started

### Prerequisites

#### Without Docker

You need to have Python (3.6.8), PIP and PostgreSQL installed. There are multiple ways to install Python, either download from the official [Python site](https://www.python.org/downloads/) or use the package manager [Homebrew](https://brew.sh/) ```brew install python3```. PIP comes installed with Python 3.4(or greater) by default.

To install Postgres you can also use [Homebrew](https://brew.sh/)

```
brew update
brew doctor
brew install postgresql
```


#### With Docker

You need to have Docker and PostgreSQL installed. Docker installation guidance can be found in the [Docker Docs](https://docs.docker.com/install/).

To install Postgres you can also use [Homebrew](https://brew.sh/)

```
brew update
brew doctor
brew install postgresql
```

### Running the database

To start Postgres:

```
pg_ctl -D /usr/local/var/postgres start && brew services start postgresql
```

Create a local database

```
CREATE DATABASE sampledb;
CREATE USER manager WITH PASSWORD 'supersecretpassword';
GRANT ALL PRIVILEGES ON DATABASE sample TO manager;
```

### Environment variables

| Variable          | Default              | Description                                 |
| ----------------- | -------------------- | ------------------------------------------- |
| DBHOST            | host.docker.internal | DB host url/string                          |
| DBPORT            | 5432                 | DB connection port                          |
| DBNAME            | <database name>      | DB name to use                              |
| DBUSER            | <username>           | DB user                                     |
| DBPASSWORD        | <password>           | DB password                                 |
| AZURE_ACCOUNT_NAME| <azureaccountname>   | The name of the account for image storage   |
| AZURE_ACCOUNT_KEY | <azureaccountkey>    | The access key to account for image storage |
| AZURE_ACCOUNT     | <azureaccount>       | The account for image storage               |
| LOCAL             | False                | Tells the site to use external API or mocks |


### Running the site

#### Running without Docker

Create a Python 3.6.8 virtual environment and run the following commands from the root directory of the project:

```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```


#### Running with Docker

```
docker-compose build
docker-compose up
```

The first command builds the docker image.
The second command starts the docker container, running on port 8000.


#### Initial access

The migrations in the `core` module will create a superuser to allow initial access to the CMS.

````
Username - superuser
Password - adminpassword
````

This can be used for accessing the system during development, but should be removed when the code is deployed to Production.

##### Useful commands

There are commands setup in the bin directory of the project, that allow easy use of common commands inside the docker container.

_These commands use the container name to access the container, this is based on the root directory name of the repository. If the directory name is changed these commands will need to be updated._

- container - takes you on to the containers command line.
- coverage - runs the unit tests with coverage reporting.
- lint - runs the code format linter against the code.
- manage - can be passed arguments to run standard django manage.py commands.
- shell - takes you on to the python shell command line for the project.
- test - runs the unit tests.



##### Adding new dependencies

Adding a new dependency requires rebuilding docker image for Django app.

Stop docker container

```
docker-compose down
```

Rebuild Docker image

```
docker-compose build
```

Start server again

```
docker-compose up
```

## Contributing

See [CONTRIBUTING](docs/CONTRIBUTING.md) for details.

## License

See [LICENSE](docs/LICENSE.md) for details.
