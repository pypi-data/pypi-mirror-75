from typing import Dict, Any, List
import enum, os, sys
import dj_database_url

from django.core.exceptions import ImproperlyConfigured


class MissingRequiredEnvVar(Exception):

    def __init__(self, envvar):
        # Call the base class constructor with the parameters it needs
        super().__init__(f"Missing required environment variable: {envvar}")

        # Now for your custom code...
        self.envvar = envvar


class Profile(enum.Enum):
    LOCAL_DEBUG = 0
    HEROKU_STAGING = 1
    HEROKU_PRODUCTION = 2


class Required(enum.Enum):
    NEVER = 0
    ON_PRODUCTION = 1
    ON_HEROKU = 2
    ALWAYS = 10

class BaseFxSettings:
    settings: Dict[str, Any] = None
    profile: Profile = None

    def __init__(self, *, base_dir):
        self.settings = {}
        self.base_dir = base_dir

        # If .env wasn't loaded by manage.py, it should be loaded by here.
        if not "SECRET_KEY" in os.environ:
            from dotenv import load_dotenv
            load_dotenv()

        # Set secret key
        self.settings["SECRET_KEY"] = self.get_env("SECRET_KEY", required=Required.ALWAYS)

    def get_env(self, name, *, default=None, required: Required = Required.ALWAYS):
        var = os.environ.get(name, None)

        if not var:

            if required == Required.ALWAYS:
                raise MissingRequiredEnvVar(name)
            elif required == Required.ON_PRODUCTION and self.is_production():
                raise MissingRequiredEnvVar(name)
            elif required == Required.ON_HEROKU and self.is_on_heroku():
                raise MissingRequiredEnvVar(name)
            else:
                return default

        return var

    def is_debug(self):
        """
        Return True if the code is run on a debug environment

        Debug environment is allowed to have lower security check. Always check is_debug before to disable any
        security settings.
        """
        if self.profile:
            if self.profile == Profile.LOCAL_DEBUG:
                return True
            else:
                return False
        else:
            return False

    def is_staging(self):
        """
        Return True if the code is run on a staging environment

        Staging environment isn't allow to have lower security check as production, but it's allowed to disable some
        integration with external third parties
        """
        if self.profile:
            if self.profile == Profile.HEROKU_STAGING:
                return True
            else:
                return False
        else:
            return False

    def is_production(self) -> bool:
        """
        Return True if the code isn't either in debug or staging mode
        """

        if self.is_debug() or self.is_staging():
            return False
        else:
            return True

    def is_on_heroku(self) -> bool:
        if not self.profile:
            raise ImproperlyConfigured("Profile wasn't set. Have you forgotten to call FxSettings.autodetect_profile?")

        if self.profile == Profile.HEROKU_STAGING:
            return True
        elif self.profile == Profile.HEROKU_PRODUCTION:
            return True
        else:
            return False

    def is_under_test(self) -> bool:
        """
        Return True if we are under "unit test" mode.
        """
        if len(sys.argv) > 1 and sys.argv[1] == 'test':
            # test detected in argv. Assuming we are running test with python admin.py test
            return True
        else:
            return False

    def autodetect_profile(self, *, choices: List[Profile]):
        """
        Autodetect the current profile

        Profile.LOCAL_DEBUG is detected if 'DJANGO_PROFILE' environment variable is set to 'DEBUG'
        :return:
        """
        DJANGO_PROFILE = os.environ.get("DJANGO_PROFILE", None)
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)

        if Profile.LOCAL_DEBUG in choices:
            if DJANGO_PROFILE == "DEBUG":
                self.settings["DEBUG"] = True
                self.profile = Profile.LOCAL_DEBUG

                # Security check: Fail if heroku is detected
                if HEROKU_APP_NAME:
                    raise ImproperlyConfigured("It's unsafe to unable DEBUG on Heroku")

                return
            else:
                pass

        if Profile.HEROKU_STAGING:
            if HEROKU_APP_NAME and HEROKU_APP_NAME.endswith("-staging"):
                self.profile = Profile.HEROKU_STAGING
                return
            else:
                pass

        if Profile.HEROKU_PRODUCTION:
            # We need to have HEROKU_APP_NAME defined:
            if not HEROKU_APP_NAME:
                raise ImproperlyConfigured(
                    "Please enable 'Heroku Labs: Dyno Metadata' by running"
                    "`heroku labs:enable runtime-dyno-metadata -a <app name>"
                )

            # Default to prod
            self.profile = Profile.HEROKU_PRODUCTION

    def save_settings(self, *, to):
        for key, value in self.settings.items():
            to[key] = value




class FxSettings(BaseFxSettings):

    def enable_sentry(self, *, required: Required, use_heroku_metadata=False):

        SENTRY_DSN = self.get_env("SENTRY_DSN", required=required)

        if SENTRY_DSN:
            # django-rq need to have access to SENTRY_DSN in settings
            self.settings["SENTRY_DSN"] = SENTRY_DSN

            if use_heroku_metadata:
                HEROKU_APP_NAME = self.get_env("HEROKU_APP_NAME", required=Required.ALWAYS)
                HEROKU_RELEASE_VERSION = self.get_env("HEROKU_RELEASE_VERSION", required=Required.ALWAYS)
                HEROKU_SLUG_COMMIT = self.get_env("HEROKU_SLUG_COMMIT", required=Required.ALWAYS)

                release = HEROKU_APP_NAME.replace("-prod", "").replace("-production", "").replace("-staging", "")
                release += "@"
                release += HEROKU_SLUG_COMMIT

                server_name = HEROKU_APP_NAME
            else:
                raise NotImplemented("Only usage with use_heroku_metadata is implemented")

            # Only import sentry if we need it
            import sentry_sdk
            from sentry_sdk.integrations.django import DjangoIntegration

            sentry_sdk.init(
                dsn=os.environ["SENTRY_DSN"],
                integrations=[DjangoIntegration()],
                release=release,
                server_name=server_name,
                environment=str(self.profile)
            )

    def set_modern_django_default(self):

        # By setting SECURE_SSL_REDIRECT = True, all page that are not listed in SECURE_REDIRECT_EXEMPT will be redirected
        # from http to https
        self.settings["SECURE_SSL_REDIRECT"] = True
        if self.is_debug():
            self.settings["SECURE_SSL_REDIRECT"] = False

        # IP allowed for Django Debug Toolbar
        self.settings["INTERNAL_IPS"] = ["127.0.0.1"]

        # Enable Internationalization and timezone
        self.settings["LANGUAGE_CODE"] = "en-us"
        self.settings["TIME_ZONE"] = "UTC"
        self.settings["USE_I18N"] = True
        self.settings["USE_L10N"] = True
        self.settings["USE_TZ"] = True
        self.settings["LOCALE_PATHS"] = (os.path.join(self.base_dir, "locale"),)

        # Common password
        # Password validation
        # https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

        self.settings["AUTH_PASSWORD_VALIDATORS"] = [
            {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
            {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
            {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
            {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
        ]

    def set_foxtron_common_settings(self):
        self.settings["ROOT_URLCONF"] = "project.urls"
        self.settings["WSGI_APPLICATION"] = "project.wsgi.application"
        self.settings["STATICFILES_DIRS"] = [os.path.join(self.base_dir, "project/static")]

        # Languages:
        self.settings["LANGUAGES"] = (("en", "English"), ("fr", "French"), ("de", "German"))

        # Static file
        self.settings["STATIC_URL"] = "/static/"
        self.settings["STATIC_ROOT"] = os.path.join(self.base_dir, 'staticfiles')

        # Email
        self.settings["DEFAULT_FROM_EMAIL"] = "noreply@foxtron.ch"
        self.settings["SERVER_EMAIL"] = "noreply@foxtron.ch"  # Email for error message
        self.settings["EMAIL_SUBJECT_PREFIX"] = "[Foxtron GmbH] "

        self.settings["CRISPY_TEMPLATE_PACK"] = "bootstrap4"

        # django-phonenumber-field
        self.settings["PHONENUMBER_DB_FORMAT"] = "E164"  # eg. "+417324891616"
        self.settings["PHONENUMBER_DEFAULT_REGION"] = "CH"

        # Error email
        self.settings["ADMINS"] = [
            ("Foxtron GmbH", "login@foxtron.ch"),
        ]

        self.settings["MANAGERS"] = [
            ("Foxtron GmbH", "login@foxtron.ch"),
        ]

    def autoconfigure_django_rq(self, *, required, async_under_test, default_timeout: int):
        REDIS_URL = self.get_env("REDIS_URL", required=required)

        if REDIS_URL:
            async_ = True

            if self.is_under_test():
                async_ = async_under_test

            self.settings["RQ_QUEUES"] = {
                'default': {
                    'URL': REDIS_URL,
                    'DEFAULT_TIMEOUT': default_timeout,
                    'ASYNC': async_,
                },
                'high': {
                    'URL': REDIS_URL,
                    'DEFAULT_TIMEOUT': default_timeout,
                    'ASYNC': async_,
                },
                'low': {
                    'URL': REDIS_URL,
                    'DEFAULT_TIMEOUT': default_timeout,
                    'ASYNC': async_,
                },
            }

    def autoconfigure_redis_cache(self, *, required):
        REDIS_URL = self.get_env("REDIS_URL", required=required)

        if REDIS_URL:
            self.settings["CACHES"] = {
                "default": {
                    "BACKEND": "django_redis.cache.RedisCache",
                    "LOCATION": REDIS_URL,
                    "OPTIONS": {
                        "CLIENT_CLASS": "django_redis.client.DefaultClient",
                    }
                }
            }

    def autoconfigure_twilio(self, *, required):

        self.settings["TWILIO_ACCOUNT_SID"] = self.get_env("TWILIO_ACCOUNT_SID", required=required)
        self.settings["TWILIO_AUTH_TOKEN"] = self.get_env("TWILIO_AUTH_TOKEN", required=required)

    def autoconfigure_sendgrid(self, *, required, fallback_backend=None):

        SENDGRID_API_KEY = self.get_env("SENDGRID_API_KEY", required=required)

        if SENDGRID_API_KEY:
            # Integrate with sendgrip using smtp
            self.settings["EMAIL_HOST"] = "smtp.sendgrid.net"
            self.settings["EMAIL_HOST_USER"] = "apikey"
            self.settings["EMAIL_HOST_PASSWORD"] = SENDGRID_API_KEY
            self.settings["EMAIL_PORT"] = 587
            self.settings["EMAIL_USE_TLS"] = True
        else:
            if fallback_backend:
                self.settings["EMAIL_BACKEND"] = fallback_backend

    def autoconfigure_s3storage(self, *,
                                required,
                                fallback_backend=None,
                                region="eu-west-1",
                                signature="s3v4",
                                location
        ):
        self.settings["AWS_ACCESS_KEY_ID"] = self.get_env("AWS_ACCESS_KEY_ID", required=required)
        self.settings["AWS_SECRET_ACCESS_KEY"] = self.get_env("AWS_SECRET_ACCESS_KEY", required=required)
        self.settings["AWS_STORAGE_BUCKET_NAME"] = self.get_env("AWS_STORAGE_BUCKET_NAME", required=required)
        self.settings["AWS_STORAGE_REGION_NAME"] = region
        self.settings["AWS_S3_SIGNATURE_VERSION"] = signature
        self.settings["AWS_LOCATION"] = location

        if self.settings.get("AWS_ACCESS_KEY_ID", None):
            self.settings["DEFAULT_FILE_STORAGE"] = 'storages.backends.s3boto3.S3Boto3Storage'
        else:
            if fallback_backend:
                self.settings["DEFAULT_FILE_STORAGE"] = fallback_backend

    def autoconfigure_database( self, *,
            required: Required,
            conn_max_age: int = 600,
            ssl_require: bool = True,
            force_postgis = False,
        ):

        DATABASE_URL = self.get_env("DATABASE_URL", required=Required)
        DATABASE_URL_TEST = self.get_env("DATABASE_URL_TEST", required=Required.NEVER)

        if self.is_under_test():
            if DATABASE_URL_TEST:
                DATABASE_URL = DATABASE_URL

        if DATABASE_URL:

            if force_postgis:
                # With force_postgis, we can use the postgis backend also when DATABASE_URL use postgres://
                # instead of postgis://
                DATABASE_URL.replace("postgres://", "postgis://")

            # Create a default database
            if 'DATABASES' not in self.settings:
                self.settings['DATABASES'] = {'default': None}

            self.settings['DATABASES']['default'] = dj_database_url.parse(
                DATABASE_URL,
                conn_max_age=conn_max_age,
                ssl_require=ssl_require)




    def enable_whitenoise(self, *, to):
        """
        This function should be called at the end of config.py
        It modify the config.py to automatically add whitnoise after in MIDDLEWARE

        If called on debug, it will add 'whitenoise.runserver_nostatic' as the first 'INSTALLED_APPS'
        """

        mw: List = list(to["MIDDLEWARE"])

        # From WhiteNoise documentation:
        # The WhiteNoise middleware should be placed directly after the Django SecurityMiddleware (if you are using it)
        # and before all other middleware:
        if "django.middleware.security.SecurityMiddleware" in mw:
            index = mw.index('django.middleware.security.SecurityMiddleware')
            mw.insert(index+1, 'whitenoise.middleware.WhiteNoiseMiddleware')
        else:
            mw.insert(0, 'whitenoise.middleware.WhiteNoiseMiddleware')


        to["MIDDLEWARE"] = mw
        to["STATICFILES_STORAGE"] = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

        if self.is_debug():
            apps: List = list(to["INSTALLED_APPS"])
            apps.insert(0, "whitenoise.runserver_nostatic")
            to["INSTALLED_APPS"] = apps
