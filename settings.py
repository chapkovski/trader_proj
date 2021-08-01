from os import environ
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TIME_ZONE = 'UTC'
default_app_seq = [
    'pretrade',
    'trader_wrapper',
    'post_experimental'

]
SESSION_CONFIGS = [

    dict(
        name='pretrade',
        display_name="Pre-trade (instructions, comprehension)",
        num_demo_participants=1,
        app_sequence=['pretrade'],

    ),
    dict(
        name='baseline',
        display_name="trader ONLY - baseline",
        num_demo_participants=1,
        app_sequence=['trader_wrapper'],
        gamified=False,

    ),

    dict(
        name='gamified',
        display_name="trader ONLY - gamified",
        num_demo_participants=1,
        app_sequence=['trader_wrapper'],
        gamified=True,
    ),

    dict(
        name='post',
        display_name="post-experimental (quiz, SES)",
        num_demo_participants=1,
        app_sequence=['post_experimental'],

    ),
    dict(
        name='full_baseline',
        display_name="FULL STUDY - baseline",
        num_demo_participants=1,
        app_sequence=default_app_seq,
        gamified=False,

    ),

    dict(
        name='full_gamified',
        display_name="FULL STUDY - gamified",
        num_demo_participants=1,
        app_sequence=default_app_seq,
        gamified=True,
    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.05, participation_fee=0.00, doc="",
    for_prolific=False,
    prolific_redirect_url='http://www.lenta.ru',
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'y(8c37tkwqf#m$gg9=z*54k&jojh6ddhlj75j4klo6evkkfwb%'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = [
    'otree',
    'webpack_loader',
    'trader_wrapper',
    'pretrade',
    'django_countries'
]
COUNTRIES_FIRST = ['US', 'GB']
COUNTRIES_FIRST_BREAK = '-------'
COUNTRIES_FIRST_REPEAT = True

WEBPACK_LOADER = {
    'DEFAULT': {
        # 'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'vue/',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'traderfront', 'webpack-stats.json'),
        'POLL_INTERVAL': 0.3,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map']
    }
}
