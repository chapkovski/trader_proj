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
import random
from django.db import models as djmodels

author = 'Philipp Chapkovski, HSE-Moscow'

doc = """
Backend for trading platform 
"""


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Constants(BaseConstants):
    name_in_url = 'trader_wrapper'
    players_per_group = None
    num_rounds = 1

    EVENT_TYPES = AttrDict(
        price_update='PRICE_UPDATE',
        tab_change='TAB_CHANGE',
        transaction='TRANSACTION',
        task_submission='TASK_SUBMITTED',

    )


class Subsession(BaseSubsession):
    def creating_session(self):
        from .utils import creating_events
        for p in self.get_players():
            creating_events(p)
            p.age = random.randint(18, 100)
            p.gender = random.choice(['Male', 'Female'])
            p.income = random.randint(0, 7)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField()
    gender = models.StringField()
    income = models.IntegerField()


class Event(djmodels.Model):
    class Meta:
        ordering = ['timestamp']

    owner = djmodels.ForeignKey(to=Player, on_delete=djmodels.CASCADE, related_name='events')
    raw = models.LongStringField()
    event_type = models.StringField()
    timestamp = djmodels.DateTimeField(null=True, blank=True)
    stock = models.StringField()
    quantity = models.FloatField()
    total_amount = models.FloatField()
    price = models.FloatField()
    task = models.LongStringField()
    answer = models.IntegerField()
    is_task_correct = models.BooleanField()
    tab_name = models.StringField()

    def __str__(self):
        return f'Event type: {self.event_type}'


def custom_export(players):
    all_fields = Event._meta.get_fields()
    field_names = [i.name for i in all_fields]
    player_fields = ['participant_code', 'age', 'gender', 'income', 'session_code', 'treatment']
    yield field_names + player_fields
    for q in Event.objects.order_by('id'):
        yield [getattr(q, f) or '' for f in field_names] + [q.owner.participant.code, q.owner.age, q.owner.gender,
                                                            q.owner.income, q.owner.session.code,
                                                            q.owner.session.config.get('display_name')]
