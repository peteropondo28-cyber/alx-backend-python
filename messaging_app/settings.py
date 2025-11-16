import os
ROOT_URLCONF = 'messaging_app.urls'


TEMPLATES = [
{
'BACKEND': 'django.template.backends.django.DjangoTemplates',
'DIRS': [],
'APP_DIRS': True,
'OPTIONS': {
'context_processors': [
'django.template.context_processors.debug',
'django.template.context_processors.request',
'django.contrib.auth.context_processors.auth',
'django.contrib.messages.context_processors.messages',
],
},
},
]


WSGI_APPLICATION = 'messaging_app.wsgi.application'


# Database
# Keep simple: sqlite by default, change DATABASE_URL in .env for production
DATABASE_URL = env('DATABASE_URL', default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")


import dj_database_url
DATABASES = {
'default': dj_database_url.parse(DATABASE_URL)
}


# Password validation (keep defaults for development)
AUTH_PASSWORD_VALIDATORS = [
{
'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
},
{
'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
},
{
'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
},
{
'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
},
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Custom user model
AUTH_USER_MODEL = 'chats.User'


# Django REST framework basic config
REST_FRAMEWORK = {
'DEFAULT_AUTHENTICATION_CLASSES': (
'rest_framework.authentication.SessionAuthentication',
'rest_framework.authentication.BasicAuthentication',
),
'DEFAULT_PERMISSION_CLASSES': (
'rest_framework.permissions.IsAuthenticatedOrReadOnly',
),
}
