"""
Django settings for opensrp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7lx599_c*gwws^)!jncu1^ir4!=ufxxttudwj09ztdey(gx=xp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'drishti',
        'USER': 'dhanush',
        'PASSWORD': 'dhanush',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
           'options': '-c search_path=report'
        }
    },
     'dynamic_data':{
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME':'test',
       'USER':'',
       'PASSWORD':''
     },
    }


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Masters',
    'multiselectfield',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'opensrp.urls'

WSGI_APPLICATION = 'opensrp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
# STATIC_ ROOT= '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ADMIN_MEDIA_PREFIX = '/static/admin/'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
DRUG_MAP = {"CHILD":0,"PNC":1,"ANC":2}
USER_ROLE={"ANM":"ROLE_USER","PHC":"ROLE_PHC_USER","DOC":"ROLE_DOC_USER"}
#STATICFILES_DIRS = (BASE_DIR + '/static/',)

DISEASES = ('Pallor',
'Swelling',
'Bleeding',
'Jaundice',
'Convulsions',
'Difficult Breathing',
'Bad Headache',
'Blurred Vision',
'Uterus is soft or tender',
'Abdominal Pain',
'Bad Smelling lochea',
'Heavy Bleeding per vaginum',
'Infected perineum suture',
'Difficulty Passing Urine',
'Burning sensation when urinating',
'Breast Hardness',
'Nipple Hardness',
'Mealses',
'Diarrhea and dehydration',
'Malaria',
'Acute Respiratory Infection',
'Severe Acute Mal Nutrition',
'Cough',
'Diarrhea',
'Fever',
'Vomiting')


INDICATORS=(("condom_usage","CONDOM USEAGE"),
            ("condom_pieces","CONDOM PIECES"),
            ("iud_adoption","IUD ADOPTION"),
            ("oral_pills","ORAL PILLS"),
            ("total_anc_registrations","Total ANC registrations"),
            ("late_anc_registrations","Late ANC registrations"),
            ("early_anc_registrations","Early ANC registrations"),
            ("tt2_booster","TT2/TT Booster"),
            ("tt1","TT1"),
            ("cesareans","Cesareans"),
            ("cesareans_gh","Cesareans Govt. hospital"),
            ("total_deliveries","Total Deliveries"),
            ("chc","Deliveries at Community Health center"),
            ("dh","Deliveries at District Health center "),
            ("bcg","BCG"),
            ("bf","BF with in 1hr of birth"),
            ("diarrhea","DIARRHEA"),
            ("hep","HEP"),
            ("infant_balance","INFANT BALANCE"),
            ("infant_balance_oa","INFANT BALANCE OA"),
            ("low_birth_weight","CHILD WITH LOW BIRTH WEIGHT"),
            ("child_weighed","CHILD_WEIGHED"),
            ("pentavalent","PENTAVALENT"),
            ("opv","OPV"),
            ("child_0_1","No. of children 0-1 years"),
            ("child_0_5","No. of children 0-5 years"),
            ("total_mother_mortality","TOTAL MOTHER MORTALITY"),
            ("anc_MaternalDeath","MOTHER MORTALITY (DURING ANC)"),
            ("anctopnc_MaternalDeath","MOTHER MORTALITY (DURING DELIVERY)"))

OPV1_PENTAVALENT1_DAYS=41
OPV2_PENTAVALENT2_DAYS=69
OPV3_PENTAVALENT3_DAYS=97
MEASLES_DAYS=269
MMR_DAYS=364
MEASLES2_DPTBOOSTER1_DAYS=539
OPVBOOSTER_DAYS=1439
DPTBOOSTER2_DAYS=1799

COUCHDB="202.153.34.169:5984"
RAPIDPROIP="202.153.34.174"

CHILD_BIRTH_WEIGHT_IN_KGS = 4

import sys
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    }

COUCHDB="202.153.34.169:5984"

try:
    from localsettings import *
except ImportError:
    pass
