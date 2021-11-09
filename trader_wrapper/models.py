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
from settings import get_game_params, get_round_params
from otree.models import Session
import random
from django.db import models as djmodels
from datetime import datetime, timedelta
from django.utils import timezone
from enum import Enum
from itertools import cycle
import os
import csv

import json
from csv import DictReader
import requests
from django.conf import settings

author = 'Philipp Chapkovski, HSE-Moscow'

doc = """
Backend for trading platform 
"""


class Constants(BaseConstants):
    name_in_url = 'trader_wrapper'
    players_per_group = None
    training_rounds = [1]
    num_rounds = len(settings.ROUND_GAME_PARAMS.keys())


def flatten(t):
    return [item for sublist in t for item in sublist]


class Subsession(BaseSubsession):
    starting_price = models.FloatField()
    tick_frequency = models.FloatField()
    max_length = models.FloatField()

    def creating_session(self):

        if self.round_number == 1:
            params = get_game_params(settings.URL_TO_READ)
            params['game_rounds'] = Constants.num_rounds
            params['round_length'] = params['tick_frequency']*params['max_length']

            round_params = get_round_params(settings.ROUND_URL_TO_READ)
            training_rounds = [k for k, v in round_params.items() if v.get('training')]
            self.session.vars['game_params'] = params

            self.session.vars['training_rounds'] = training_rounds
            self.session.vars['round_params'] = round_params
            assert (Constants.num_rounds - len(
                training_rounds)) % 2 == 0, 'Number of payble rounds should be even (so we can split them into gamified and nongamified'
            half = int((Constants.num_rounds - len(training_rounds)) / 2)
            treatment_order = [True] * half + [False] * half
            tcycle = cycle([-1, 1])
            for p in self.session.get_participants():
                p.vars['treatments'] = treatment_order[::next(tcycle)]
                lb = max(Constants.training_rounds)
                p.vars['payable_round'] = random.randint(lb + 1, Constants.num_rounds)
        for k, v in self.session.vars['game_params'].items():
            if hasattr(self, k):
                setattr(self, k, v)
        for p in self.get_players():
            p.payable_round = p.participant.vars['payable_round'] == p.round_number
            p.training = p.round_number in self.session.vars['training_rounds']
            if p.training:
                p.gamified = False
            else:
                p.gamified = p.participant.vars['treatments'][self.round_number - len(Constants.training_rounds) - 1]
            p.crash_probability = self.session.vars['round_params'][self.round_number].get('crash_probability')


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
        timestamp = timezone.now()
        self.events.create(
            part_number=self.round_number,
            owner=self,
            timestamp=timestamp,
            source='client',
            name=data.pop('name', ''),
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
