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
from dateutil.relativedelta import relativedelta
from .prices import get_prices
import os
import csv
from itertools import product
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


import requests


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Constants(BaseConstants):
    name_in_url = 'trader_wrapper'
    players_per_group = None
    trading_day_duration = 5  # in minutes
    day_length_in_seconds = 10
    tick_frequency_in_secs = 5
    num_ticks = int(day_length_in_seconds/tick_frequency_in_secs)
    tick = 5  # how often prices are updated (in seconds)
    stocks = ['A', 'B', 'ETF_A', 'ETF_B']
    tabs = ['work', 'trade']
    default_tab = 'trade'
    endowment = 0

    num_rounds = 1
    with open("data/day_params.csv") as csvfile:
        day_params = list(DictReader(csvfile))

    wages = [10, 20]
    fees = [0, 1]
    wages_fees = list(product(wages, fees))
    stocks_with_params = [
        dict(name='A',
             initial=1,
             sigma=0.2,
             leverage=1),
        dict(name='B',
             initial=1,
             sigma=0.4,
             leverage=1
             ),
        dict(name='ETF_A',
             initial=1,
             sigma=0.2,
             leverage=3
             ),
        dict(name='ETF_B',
             initial=1,
             sigma=0.4,
             leverage=3
             ),
    ]
    awards = {1: dict(name='First transaction',
                      message='Hooray! you have made your first transaction!'),
              3: dict(name='Bronze', message='Three transactions! That\'s the spirit!'),
              5: dict(name='Silver', message='Incredible, George Soros wishes you luck!'),
              10: dict(name='Gold', message='Warren Buffet envies you!')}


class Subsession(BaseSubsession):
    params = models.LongStringField()

    def get_params(self):
        return json.loads(self.params)

    def creating_session(self):

        if self.round_number == 1:
            for p in self.session.get_participants():
                wages_fees = [val for val in Constants.wages_fees for _ in (0, 1)]
                p.vars['wages_fees'] = wages_fees

        for p in self.get_players():
            p.current_stock_shown = random.choice(Constants.stocks)
            p.current_tab = Constants.default_tab
            if self.round_number == 1:
                p.start_time = timezone.now()
            else:
                p.start_time = p.in_round(self.round_number - 1).end_time + timedelta(seconds=30)
            p.end_time = p.start_time + timedelta(minutes=Constants.trading_day_duration)
            # p.generate_deposit()  # TODO: in production move to bulk update right here
            # p.generate_prices()  # TODO: in production move to bulk update right here
            p.endowment = Constants.endowment  # we may randomize it later, let's keep it simple for now.
            p.starting_balance = p.endowment
            p.ending_balance = p.endowment
            # the below thing is ugly AF, but tbh i dont care
            p.wage = p.participant.vars.get('wages_fees')[p.round_number - 1][0]
            p.transaction_fee = p.participant.vars.get('wages_fees')[p.round_number - 1][1]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    """In production we may not need theses two fields, but it is still useful to have them
    as natural limits after which the player should proceed to the next trading day.
    """
    start_time = djmodels.DateTimeField(null=True, blank=True)
    end_time = djmodels.DateTimeField(null=True, blank=True)
    current_stock_shown = models.StringField(doc='registers сurrent stock shown to a player')
    current_tab = models.StringField(doc='registers current tab the player is it')
    endowment = models.FloatField(doc='initial amount given to a participant at the beginning of the trading day')
    starting_balance = models.FloatField(doc='to store the initial state of bank account')
    ending_balance = models.FloatField(
        doc='to store the final (for a specific trading day  aka round) state of bank account')
    wage = models.FloatField(doc='How much they earn for submitting the correct fee')
    transaction_fee = models.FloatField(doc='Transaction fee per trade')
    num_tasks_submitted = models.IntegerField(doc='to store number of total tasks submitted', initial=0)
    num_correct_tasks_submitted = models.IntegerField(doc='to store number of correct tasks submitted',
                                                      initial=0)

    def register_event(self, data):
        print('WE GET THE DATA', data)
        timestamp = timezone.now()
        balance = float(data.pop('balance', 0))
        self.events.create(owner=self,
                           timestamp=timestamp,
                           source='client',
                           name=data.pop('name', ''),
                           balance=balance,
                           round_number=data.pop('round_number', None),
                           body=json.dumps(data),
                           )
        return {
            self.id_in_group: dict(timestamp=timestamp.strftime('%m_%d_%Y_%H_%M_%S'), action='getServerConfirmation')}


class Event(djmodels.Model):
    class Meta:
        ordering = ['timestamp']

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
                     'wage',
                     'transaction_fee',
                     'session_code',
                     'treatment']
    yield field_names + player_fields
    for q in Event.objects.filter(owner__session=session).order_by('owner__session', 'owner__round_number',
                                                                   'timestamp'):
        yield [getattr(q, f) or '' for f in field_names] + [q.owner.participant.code,
                                                            q.owner.wage,
                                                            q.owner.transaction_fee,
                                                            q.owner.session.code,
                                                            q.owner.session.config.get('display_name')]
