"""
Django settings for middle_school_system project.
"""

import os
from pathlib import Path
from decouple import config, Csv
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-this')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# Application definition
INSTALLED_APPS = [
    'simpleui',  # 必须放在django.contrib.admin之前
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 第三方应用
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
    # 本地应用
    'apps.users',
    'apps.courses',
    'apps.exercises',
    'apps.ai_services',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS中间件，必须在CommonMiddleware之前
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'middle_school_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'middle_school_system.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='middle_school_system'),
        'USER': config('DB_USER', default='alex'),
        'PASSWORD': config('DB_PASSWORD', default='123456'),
        'HOST': config('DB_HOST', default='192.168.184.130'),
        'PORT': config('DB_PORT', default='3307'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'  # 中文

TIME_ZONE = 'Asia/Shanghai'  # 上海时区

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',  # 默认允许所有，在view中单独控制
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'EXCEPTION_HANDLER': 'utils.exceptions.custom_exception_handler',
}

# JWT配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# CORS配置
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:8501,http://127.0.0.1:8501',
    cast=Csv()
)
CORS_ALLOW_CREDENTIALS = True

# 加密密钥
ENCRYPTION_KEY = config('ENCRYPTION_KEY', default='')

# 学校配置（默认为空，用户可自行输入）
DEFAULT_SCHOOL = config('DEFAULT_SCHOOL', default='')

# SimpleUI配置
SIMPLEUI_CONFIG = {
    'system_keep': False,
    'menu_display': ['用户管理', '课程管理', '练习题管理', 'AI服务'],
    'dynamic': True,
    'menus': [
        {
            'name': '用户管理',
            'icon': 'fas fa-users',
            'models': [
                {
                    'name': '用户列表',
                    'icon': 'fa fa-user',
                    'url': 'auth/user/'
                },
                {
                    'name': '用户资料',
                    'icon': 'fa fa-id-card',
                    'url': 'users/userprofile/'
                },
                {
                    'name': 'AI配置',
                    'icon': 'fa fa-robot',
                    'url': 'users/aiconfig/'
                }
            ]
        },
        {
            'name': '课程管理',
            'icon': 'fas fa-book',
            'models': [
                {
                    'name': '学科管理',
                    'icon': 'fa fa-bookmark',
                    'url': 'courses/subject/'
                },
                {
                    'name': '课程管理',
                    'icon': 'fa fa-book-open',
                    'url': 'courses/course/'
                },
                {
                    'name': '知识点总结',
                    'icon': 'fa fa-lightbulb',
                    'url': 'courses/knowledgesummary/'
                },
                {
                    'name': '学习进度',
                    'icon': 'fa fa-chart-line',
                    'url': 'courses/studyprogress/'
                }
            ]
        },
        {
            'name': '练习题管理',
            'icon': 'fas fa-tasks',
            'models': [
                {
                    'name': '练习题库',
                    'icon': 'fa fa-question-circle',
                    'url': 'exercises/exercise/'
                },
                {
                    'name': '答题记录',
                    'icon': 'fa fa-clipboard-check',
                    'url': 'exercises/answerrecord/'
                }
            ]
        },
        {
            'name': 'AI服务',
            'icon': 'fas fa-robot',
            'models': [
                {
                    'name': 'Prompt模板',
                    'icon': 'fa fa-file-code',
                    'url': 'ai_services/prompttemplate/'
                },
                {
                    'name': '使用日志',
                    'icon': 'fa fa-history',
                    'url': 'ai_services/promptusagelog/'
                }
            ]
        }
    ]
}

SIMPLEUI_DEFAULT_THEME = 'admin.lte.css'
SIMPLEUI_HOME_INFO = True
SIMPLEUI_HOME_QUICK = True
SIMPLEUI_HOME_ACTION = True
SIMPLEUI_ANALYSIS = False  # 关闭SimpleUI使用分析

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}

# 确保logs目录存在
(BASE_DIR / 'logs').mkdir(exist_ok=True)

