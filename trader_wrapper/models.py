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
    num_rounds = 1

    with open("data/day_params.csv") as csvfile:
        day_params = list(DictReader(csvfile))


from itertools import cycle
import urllib.request
import yaml


def flatten(t):
    return [item for sublist in t for item in sublist]



class Subsession(BaseSubsession):
    params = models.LongStringField()

    def creating_session(self):
        orders = [[True, False], [False, True]]
        cyorders = cycle(orders)
        contents = urllib.request.urlopen(
            "http://raw.githubusercontent.com/chapkovski/trader_proj/main/data/params.yaml").read()
        c = yaml.load(contents, Loader=yaml.FullLoader)
        gps = c.copy()


        num_days = gps.get('num_days', 5)
        training_wage = gps.get('training_wage', 5)
        commission = gps.get('commission', 0)
        wages = gps.get('wages', [1, 10])
        treatment_size = int((num_days - 1) / 2)
        assert num_days % 2 == 1, 'Number of trading days should be an odd number'
        assert num_days == 1 or treatment_size == len(wages), 'Please check the length of wages parameter - it should contain the wages' \
                                             ' for each trading day'

        for p in self.get_players():
            day_params = [dict(round=1, gamified=False, wage=training_wage, commission=commission)]
            treatment_chunks = [[False, False], [True, True]]
            random.shuffle(treatment_chunks)

            treatment_chunks = flatten(treatment_chunks)
            treatment_chunks = treatment_chunks
            wages_chunks = flatten([random.sample(wages, len(wages))] * 2)
            res = [dict(wage=wage, gamified=gamified, commission=commission) for wage, gamified in
                   zip(wages_chunks, treatment_chunks)]
            for i, j in enumerate(res, start=2):
                j['round'] = i
            day_params.extend(res)
            p.day_params = json.dumps(day_params)


    def get_params(self):
        return json.loads(self.params)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    """In production we may not need theses two fields, but it is still useful to have them
    as natural limits after which the player should proceed to the next trading day.
    """


    start_time = djmodels.DateTimeField(null=True, blank=True)
    end_time = djmodels.DateTimeField(null=True, blank=True)
    payable_round = models.IntegerField()
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
        day_params = general_params(player=self).get('day_params')

        num_rounds = len(day_params)

        if num_rounds > 1:
            self.payable_round = random.randint(2, num_rounds)
        else:
            self.payable_round = 1  ## it's an ugly fix for debugging only.
        last_event_in_payable_round = self.events.filter(round_number=self.payable_round,
                                                         balance__isnull=False).latest()
        self.payoff = last_event_in_payable_round.balance
        self.participant.vars['chosen_round'] = self.payable_round
        self.participant.vars['trading_payoff'] = self.payoff


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
