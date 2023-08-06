import environ
from django.conf import settings

env = environ.Env()


def pytest_configure():
    settings.configure(
        DEBUG=True,
        SECRET_KEY="thisisthesecretkey",
        MIDDLEWARE_CLASSES=(
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ),
        INSTALLED_APPS=("herbie_core", "django.contrib.contenttypes", "django.contrib.auth",),
    )
