from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Q(Page):
    form_model = 'player'
    form_fields = ['gender',
                   'age',
                   'nationality',
                   'email',
                   'education',
                   'study_major',
                   'course_financial',
                   'experiment_before',
                   'trading_experience',
                   'online_trading_experience',
                   'trading_frequency',
                   'portfolio_frequency',
                   'asset_class',
                   'use_leverage',
                   'purpose',
                   'difficulty']


page_sequence = [
    Q,

]
