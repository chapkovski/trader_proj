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
from otree.models import Session
import random
from django.db import models as djmodels
from datetime import datetime, timedelta
from django.utils import timezone
from enum import Enum
from pretrade.models import general_params
import os
import csv

import json
from csv import DictReader

author = 'Philipp Chapkovski, HSE-Moscow'

doc = """
Backend for trading platform 
"""


class UpdSession(Session):
    class Meta:
        proxy = True

    def export_data(self):
        # TODO: this function should  write files to S3 (preferrably)
        origin = Session.objects.get(code=self.code).config

        ps = Player.objects.filter(session__code=self.code)
        export_path = datetime.now().strftime('__temp_mock_%m_%d_%Y')

        os.makedirs(export_path, exist_ok=True)
        with open(f'{export_path}/{origin.get("name")}_{self.code}.tsv', "w") as file1:
            writes = csv.writer(file1, delimiter='\t', quoting=csv.QUOTE_ALL)
            writes.writerows(custom_export(ps))


class EventType(str, Enum):
    transaction = 'transaction'
    task = 'submit_task'
    change_stock_tab = 'change_stock_tab'
    change_tab = 'change_tab'


class SourceType(str, Enum):
    inner = 'inner'
    client = 'client'


class Direction(int, Enum):
    buy = 1
    sell = -1


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Constants(BaseConstants):
    name_in_url = 'trader_wrapper'
    players_per_group = None
    trading_day_duration = 5  # in minutes
    day_length_in_seconds = 180
    tick_frequency_in_secs = 5
    work_dict_length = 6  # these two parameters define the difficulty of decoding task
    task_length = 4  # these two parameters define the difficulty of decoding task
    bonus_probability_coef = 1  ## multiplies secs_spent_in_trade/total_time by this factor to change the  probability to get extra stocks
    num_stocks_in_bonus = 1  ## number of stocks provided as bonus
    num_ticks = int(day_length_in_seconds / tick_frequency_in_secs)
    endowment = 0
    crash_probabilities = [0.01, 0.02, 0.03, 0.05]
    training_rounds = [1]
    num_rounds = len(crash_probabilities)

    with open("data/day_params.csv") as csvfile:
        day_params = list(DictReader(csvfile))


from itertools import cycle
import urllib.request
import yaml


def flatten(t):
    return [item for sublist in t for item in sublist]


from pprint import pprint


class Subsession(BaseSubsession):
    params = models.LongStringField()

    def creating_session(self):
        for p in self.session.get_participants():
            lb = max(Constants.training_rounds)
            p.vars['payable_round'] = random.randint(lb + 1, Constants.num_rounds)

        for p in self.get_players():
            p.payable_round = p.participant.vars['payable_round'] == p.round_number
            p.training = p.round_number in Constants.training_rounds
            p.crash_probability = Constants.crash_probabilities[self.round_number - 1]

    def get_params(self):
        return json.loads(self.params)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    """In production we may not need theses two fields, but it is still useful to have them
    as natural limits after which the player should proceed to the next trading day.
    """

    def formatted_prob(self):
        return f"{self.crash_probability:.0%}"

    gamified = models.BooleanField(initial=False)
    exit_price = models.FloatField()
    training = models.BooleanField()
    crash_probability = models.FloatField()
    start_time = djmodels.DateTimeField(null=True, blank=True)
    end_time = djmodels.DateTimeField(null=True, blank=True)
    payable_round = models.BooleanField()
    day_params = models.LongStringField()

    def register_event(self, data):
        print('WE GET THE DATA', data)
        timestamp = timezone.now()
        balance = float(data.pop('balance', 0))
        self.events.create(
            part_number=self.round_number,
            owner=self,
            timestamp=timestamp,
            source='client',
            name=data.pop('name', ''),
            balance=balance,
            round_number=data.pop('round_number', None),
            body=json.dumps(data),
        )

        return {
            self.id_in_group: dict(timestamp=timestamp.strftime('%m_%d_%Y_%H_%M_%S'), action='getServerConfirmation')}

    def set_payoffs(self):
        if self.payable_round:
            self.payoff = self.exit_price


class Event(djmodels.Model):
    class Meta:
        ordering = ['timestamp']
        get_latest_by = 'timestamp'

    part_number = models.IntegerField()
    owner = djmodels.ForeignKey(to=Player, on_delete=djmodels.CASCADE, related_name='events')
    source = models.StringField(doc='can be either inner (due to some internal processes) or from client')
    name = models.StringField()
    timestamp = djmodels.DateTimeField(null=True, blank=True)
    body = models.StringField()
    balance = models.FloatField()  # to store the current state of bank account
    round_number = models.IntegerField()


def custom_export(players):
    session = players[0].session
    all_fields = Event._meta.get_fields()
    field_names = [i.name for i in all_fields]

    player_fields = ['participant_code',
                     'session_code',
                     'treatment']
    yield field_names + player_fields
    for q in Event.objects.all().order_by('owner__session', 'owner__round_number',
                                          'timestamp'):
        yield [getattr(q, f) or '' for f in field_names] + [q.owner.participant.code,

                                                            q.owner.session.code,
                                                            q.owner.session.config.get('display_name')]
