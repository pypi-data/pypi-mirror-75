# Google Pubsub Adapter

This Adapter is based on Django and provides a way to publish messages to Google Pubsub.

It is meant to be used with [Herbie](https://github.com/herbie/herbie).

The package already provides a Django app that just needs to be registered in the main Django app using Herbie.

## Installation

1. Run the following

```
    pip install herbie-google-pubsub-adapter
```

or add it to your app `requirements.txt` and update them running:

```
    pip install -r requirements.txt
```

2. Add the adapter App to `Django Installed Apllications`:

```
    INSTALLED_APPS = [
        ...
        'google_pubsub_adapter.apps.HerbieGooglePubsubAdapterConfig',
        ...
    ]
```

3. Add your Google Cloud Pubsub Credentials to the `django settings` file:

```
GCLOUD_PUBSUB_PROJECT_ID='pubsub_project_id'
```

4. Create the Topics according to the Business Schemas

```
python manage.py init_pubsub
```

An example Django application using this adapter can be found at the [Herbie Sandbox](https://github.com/herbie/sandbox) repository.

## Developing/Testing

If you would like to further improve this package you'll need to install the dev/test requirmeents. 

To to this run in your `virtual environment`

```
    pip install -e .[tests]
```

This will install the needed packages (e.g: `pytest`) to run/test locally the package

### Black Formatter

This package uses [Black](https://github.com/psf/black) as a code formatter. You should run it before 
pushing the code as the CI pipeline checks against it.

```
    black --line-length 119 .
```
