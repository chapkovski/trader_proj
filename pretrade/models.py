from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import json
from django.db import models as djmodels
from pprint import pprint
import yaml

author = 'Philipp Chapkovski, HSE Moscow, chapkovski@gmail.com'

doc = """
Instructions, comprehension check for trader
"""


class Constants(BaseConstants):
    name_in_url = 'pretrade'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    cq1 = models.StringField(
        label="When can you switch between “Trade” and “Work” tabs?",
        choices=["Only at the beginning of the round",
                 "Only 1 minute of trading",
                 "At any point during the round",
                 "Only two switches are allowed in each round.",
                 ],
        widget=widgets.RadioSelect
    )

    def cq1_error_message(self, value):
        if value != 'At any point during the round':
            return 'Wrong answer!'
