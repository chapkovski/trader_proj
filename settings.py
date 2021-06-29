from os import environ
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TIME_ZONE = 'UTC'
SESSION_CONFIGS = [
    dict(
        name='baseline',
        display_name="trader - baseline",
        num_demo_participants=1,
        app_sequence=['trader_wrapper'],
        gamified=False,

    ),

    dict(
        name='gamified',
        display_name="trader - gamified",
        num_demo_participants=1,
        app_sequence=['trader_wrapper'],
        gamified=True,
    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
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
]

WEBPACK_LOADER = {
    'DEFAULT': {
        'STATS_FILE': os.path.join(BASE_DIR, 'traderfront', 'webpack-stats.json'),
    }
}