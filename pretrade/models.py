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
    pass
