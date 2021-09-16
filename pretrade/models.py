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
from csv import DictReader

author = 'Philipp Chapkovski, HSE Moscow, chapkovski@gmail.com'

doc = """
Instructions, comprehension check for trader
"""
with open(r'./data/params.yaml') as file:
    _general_params = yaml.load(file, Loader=yaml.FullLoader)
with open("data/day_params.csv") as csvfile:
    _day_params = list(DictReader(csvfile))
import urllib.request


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

    cq2 = models.StringField(
        label="If 5-second returns on Stock A and Stock B are -3% and 1.5% respectively, the corresponding 5-second "
              "leveraged ETF returns are:",
        choices=["9% and 4.5%",
                 "9% and -4.5%",
                 "-9% and 4.5%",
                 "-9% and -4.5%",
                 ],
        widget=widgets.RadioSelect
    )

    cq3 = models.StringField(
        label="What carries over between rounds?",
        choices=["Your trading portfolio",
                 "Your bank account balance",
                 "Both your portfolio and your bank account balance",
                 "Neither your portfolio nor your account balance",
                 ],
        widget=widgets.RadioSelect
    )

    cq4 = models.StringField(
        label="Your total bonus payment for the experiment depends on:",
        choices=["Your trading profit across all rounds",
                 "Your trading profit and total work wages in a randomly selected round",
                 "Your trading profit in a randomly selected round",
                 "Your trading profit and total work wages across all rounds",
                 ],
        widget=widgets.RadioSelect
    )

    def cq1_error_message(self, value):
        if value != 'At any point during the round':
            return 'Wrong answer!'

    def cq2_error_message(self, value):
        if value != '-9% and 4.5%':
            return 'Wrong answer!'

    def cq3_error_message(self, value):
        if value != 'Neither your portfolio nor your account balance':
            return 'Wrong answer!'

    def cq4_error_message(self, value):
        if value != 'Your trading profit and total work wages in a randomly selected round':
            return 'Wrong answer!'
def general_params(player: Player):
    gamified = getattr(player, 'gamified',False)
    subsession=player.subsession
    contents = urllib.request.urlopen(
        "http://raw.githubusercontent.com/chapkovski/trader_proj/main/data/params.yaml").read()
    c = yaml.load(contents, Loader=yaml.FullLoader)
    gps = c.copy()
    # gps = _general_params.copy() # UNCOMMENT FOR LOCAL testing

    numTicks = gps.get('dayLength') / gps.get('tickFrequency')
    _day_params = json.loads(getattr(player, 'day_params', "{}"))

    injected = dict(
                    numTicks=numTicks,
                    day_length_in_min=gps.get('dayLength') / 60,
                    num_rounds=len(_day_params),
                    real_world_currency_per_point=subsession.session.config.get('real_world_currency_per_point'),
                    example_work_time_min=gps.get('dayLength') / 60 - gps.get('example_time_min'),
                    formatted_prob=gps.get('bonusProbabilityCoef') * 100,
                    example_formatted_prob=(gps.get('example_time_min') / (gps.get('dayLength') / 60) * gps.get(
                        'bonusProbabilityCoef')) * 100,
                    day_params=_day_params
                    )
    return dict(**gps, **injected)