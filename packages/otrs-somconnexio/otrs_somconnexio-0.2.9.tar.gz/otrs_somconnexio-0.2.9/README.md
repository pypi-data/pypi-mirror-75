# Python 2.7 module to manage the SomConnexio's ERP integration with OTRS

## Functionalities

* Create OTRS ADSL provision ticket.
* Create OTRS Fibre provision ticket.
* Update ADSL/Fibre ticket with the content of coverage tickets related with the customer.
* Get tickets information (with ticket id).
* Search tickets: https://pyotrs.readthedocs.io/en/latest/readme.html#search-for-tickets

WIP:
* Create OTRS mobile provision ticket.

## OTRS Configuration

Configure a new web service in OTRS using the template provided by the PyOTRS client: https://gitlab.com/rhab/PyOTRS/-/blob/master/webservices_templates/GenericTicketConnectorREST.yml

## Objects

### OTRSClient

Client to interact with OTRS. You need to define the next environment variables to use the client:

```
OTRS_URL=       # Baseurl of the OTRS instance
OTRS_USER=      # Creadencials of user with write acces to OTRS
OTRS_PASSW=
```

### Exceptions

* TicketNotCreated
* ErrorCreatingSession
* TicketNotFoundError
* OTRSIntegrationUnknownError

### ADSL Ticket
### Fibre Ticket

## Python version

We are using [Pyenv](https://github.com/pyenv/pyenv) to fix the Python version and the virtualenv to test the package.

You need:

* Intall and configure [`pyenv`](https://github.com/pyenv/pyenv)
* Install and configure [`pyenv-virtualenvwrapper`](https://github.com/pyenv/pyenv-virtualenvwrapper)
* Intall locally the version of python needed:

```
$ pyenv install 3.8.2
```

* Create the virtualenv to use:

```
$ pyenv virtualenv 3.8.2 otrs_somconnexio
```


## Python packages requirements

Install the Python packages in the virtual environment:

```
$ pyenv exec pip install -r requirements.txt
```

## Run tests

To run the test you can run:

```
$ tox
```

Also you can run only the tests running:

```
$ python setup.py test
```

If running the tests with tox, they will be tested with both python3.8 and python2.7. This is because OTRS-SomConnexio works with an ERP which uses python2, as well as with other packages that use python3.