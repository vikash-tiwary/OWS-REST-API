Boilerplate for Flask applications
=====================================

The boilerplate defines the basic structure of flask applications that will
live in AWS Fargate. This boilerplate, in addition to the classic
python stack, includes support for Datadog, Sentry, and Loggly.

## Getting Started

### Installation

Before starting make sure you have python3.8 installed.
An easy way to manage python versions is with pyenv.
```bash
$ brew update
$ brew install pyenv
$ pyenv install 3.8
$ pyenv local 3.8
```

```bash
$ cd ows-REST-Api
$ make pip_dev
$ pre-commit install
```

### Permissions

In PROD and QA environments, to accept and authorize incoming and outgoing
requests, make sure you have the right DynamoDB permissions, as highlighted
in the corresponding [tech design](https://docs.google.com/document/d/1eHoI_BddTFMi15yCaHS6KvhSSoTrMEd3WwJINIpgNpM/edit).

### Running

When all dependencies have been installed, you can run the flask application
on your local instance by running:

```bash
(env) $ python dev.py
```

or

```bash
make dev
```
All make commands will automatically install all dependencies in an virtual environment folder called env.
You can activate a virtual environment by running `. env/bin/activate` or `source env/bin/activate`.

By using the development server, you will have access to specific features that
are not necessarily available in production, such as the exception tracer.

### Testing

To run the tests, all you have to do is to run:

```bash
(env) $ py.test tests/unit/
(env) $ py.test tests/integration/
(env) $ flake8 api/ tests/
```

or

To run unit tests: `make test`

To run unit tests with coverage reporting: `make test_unit`

To run integration tests: `make test_integration`

To lint: `make lint`

### Updating

To install new dependencies.

```bash
(env) $ pip install -r requirements-dev.txt
```

or

```bash
make pip_dev
```

### Building Docker Image
You may want to debug or verify the docker image build process is working, here's how.

:warning: Don't use this process for feature development.

1. Make sure you've got [awscli v2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) installed
```
$ aws --version
```

2. Download the [aws mfa enabled credentials generator script](https://github.com/theorchard/collab/blob/master/jcarrion/aws-creds-generator/generate.sh), and then navigate to directory containing script

3. Run the credentials generated script, selecting **dev** and inputting your mfa code
```bash
$ ./generate.sh
```

4. Set shell to use newly generated credentials
```bash
$ AWS_PROFILE=default
```

5. Set **dev** aws ecr credentials for your local docker install
```bash
$ aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 103233932089.dkr.ecr.us-east-1.amazonaws.com
```

6. Build image
```bash
$ docker build --build-arg AWS_ACCOUNT=103233932089 -t ows-REST-Api:dev .
```

7. Run most recently built image, mapping 8080 in container to 5000 on host
```bash
$ docker run -p 5000:8080 -e PORT=8080 ows-REST-Api:dev
```

8. Test application
```bash
$ curl --request GET --url http://localhost:5000/hello/
```

### Notes

Windows users will not be able to use the `make` commands as Make is a Unix util.
Windows users can attempt to install [GNUWin](http://gnuwin32.sourceforge.net/packages/make.htm) to get this functionality.

## Features of the Boilerplate

### Linting

This boilerplate comes with customization on flake8 plugins. Please make sure you keep any derivative flask microservices in-sync with these standards, as they are added.

### Third-Party Integrations for Reporting

This boilerplate comes with support for Loggly, Sentry, and Datadog.

### Grass Access Validation

The boilerplate includes module `validation.access` which contains functionality for validating Grass headers in the context of a Flask request. This is valuable for making microservice endpoints compatible for both Grass and non-Grass (i.e. microservice-to-microservice) requests. It makes it easier to facilitate endpoint reuse.

For example, suppose you need to validate that a request where Grass headers are required. Additionally, the `vendor_id` passed in the route must match - thus the Grass Account Type must be 'vendor' and the Grass Account Id must match `vendor_id`. You would use as follows:

```python
@app.route('/vendor/<vendor_id>/something')
def do_something_only_for_vendors(vendor_id):
    """Do something only for vendors.

    Args:
        vendor_id (int): unique identifier for vendor.
    """

    validation = access.verify_grass_access(
        request, required=True, vendor=vendor_id)
    if not validation:
        return validation

    // do something
```

Another example - suppose Grass headers are not required. Additionally, the `subaccount_id` passed in the route must match. The only acceptable Account Type is subaccount:

```python
@app.route('/subaccount/<subaccount_id>/something')
def do_something_only_for_subaccounts(subaccount_id):
    """Do something only for subaccounts.

    Args:
        subaccount_id (int): unique identifier for subaccount.
    """

    account_type, account_id = access.get_grass_headers(request)
    validation = access.verify_grass_access(
        request, required=False, subaccount=subaccount_id)
    if not validation:
        return validation

    // do something
```

Now, building on the last example, we can accept Account Type of vendor AND subaccount:

```python
@app.route('/subaccount/<subaccount_id>/something')
def do_something(subaccount_id):
    """Do something.

    Args:
        subaccount_id (int): unique identifier for subaccount.
    """

    account_type, account_id = access.get_grass_headers(request)
    validation = access.verify_grass_access(
        request, required=False, vendor=account_id, subaccount=subaccount_id)
    if not validation:
        return validation

    // do something
```
