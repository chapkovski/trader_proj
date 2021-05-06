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
from datetime import datetime, timedelta
from django.utils import timezone
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
    trading_day_duration = 5  # in minutes
    tick = 5  # how often prices are updated (in seconds)
    stocks = ['A', 'B', 'ETF_A', 'ETF_B']
    tabs = ['work', 'trade']
    default_tab = 'trade'
    endowment = 100
    EVENT_TYPES = AttrDict(
        price_update='PRICE_UPDATE',
        tab_change='TAB_CHANGE',
        transaction='TRANSACTION',
        task_submission='TASK_SUBMITTED',

    )


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.current_stock_shown = random.choice(Constants.stocks)
            p.current_tab = Constants.default_tab
            p.start_time = timezone.now()
            p.end_time = p.start_time + timedelta(minutes=Constants.trading_day_duration)
            p.generate_deposit()  # TODO: in production move to bulk update right here
            p.generate_prices()  # TODO: in production move to bulk update right here
            p.endowment = Constants.endowment  # we may randomize it later, let's keep it simple for now.


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
    balance = models.FloatField(doc='to store the current state of bank account')
    ########### BLOCK: post experimental survey quesitons.  ##############################################################
    # TODO: move to a separate app in production
    age = models.IntegerField()
    gender = models.StringField()
    income = models.IntegerField()

    ############ END OF: post experimental survey quesitons.  #############################################################
    def register_event(self, data):
        """That's the main manager that processes all events that arrive from frontend (and from mocking simulator)"""
        # TODO: from frontent apparentley will need to parse the date from string.
        self.events.create(**data)

    def get_price(self, stock_name):
        # TODO: somewhere here we inject proper price generation, right now just a random uniform
        return random.random()

    def generate_prices(self):
        """we bulk create price updates here.
        The trick is that also in production we pre-generate a flow of prices BEFORE the trading day starts
        with corresponding timestamps. Then we feed them every time we get a price_update request from a client.
        That we guarantee the fastest possible reaction.
        """
        t = self.start_time
        ps = []
        while t < self.end_time:
            for i in Constants.stocks:
                ps.append(Price(name=i, price=self.get_price(i), timestamp=t, owner=self))
            t = t + timedelta(seconds=Constants.tick)
        # TODO: we may limit quantity here for sqlite (it overloads with too long queries)
        Price.objects.bulk_create(ps)

    def generate_deposit(self):
        """a temporary solution to generate initial set of stocks to keep track of attainability of purchases/sales.
        in production: return a bunch of deposit objects so they can created in a huge bulk_create for the entire
        session, not for a single user, which can make it slower than we want.
        """
        for i in Constants.stocks:
            # TODO: bulk creation of Deposits here
            stonks = [Deposit(name=i, owner=self, quantity=0)]
            Deposit.objects.bulk_create(stonks)

    def latest_timestamp(self):
        """gives a latest possible timestamp"""
        # TODO: this one to be used in production to send a signal that session is over
        pass

    def get_current_task(self, timestamp):
        """TODO: timestamp should be removed in production and substituted by real time"""
        tasks = self.tasks.filter(answer__isnull=True)
        if tasks.exists():
            return tasks.latest()
        task_body = self.precreating_task(timestamp)
        t = Task.objects.create(task_body)
        return t

    def precreating_task(self, t):
        """TODO: In production returns two"""
        return dict(body='',
                    correct_answer='asdf',
                    timstamp=t,
                    owner=self)

    def price_request(self, timestamp):
        """Returns a dict of recent prices that are earlier than a given timestamp"""
        most_recent_time_stamp = self.prices.filter(timestamp__lte=timestamp).latest()
        # we use here the fact N stock prices are pre-created in waves in groups of 4
        # TODO: somewhere here in production we should check that the trading session is not over
        return self.prices.filter(timestamp=most_recent_time_stamp).values('name', 'price', 'timestamp')


class Price(djmodels.Model):
    class Meta:
        get_latest_by = 'timestamp'

    name = models.StringField()
    price = models.FloatField()
    timestamp = djmodels.DateTimeField(null=True, blank=True)
    owner = djmodels.ForeignKey(to=Player, on_delete=djmodels.CASCADE, related_name='prices')


class Deposit(djmodels.Model):
    owner = djmodels.ForeignKey(to=Player, on_delete=djmodels.CASCADE, related_name='deposit')
    quantity = models.IntegerField()
    name = models.StringField()


class Task(djmodels.Model):
    class Meta:
        ordering = ['timestamp']

    owner = djmodels.ForeignKey(to=Player, on_delete=djmodels.CASCADE, related_name='tasks')
    body = models.StringField()
    correct_answer = models.StringField()
    answer = models.StringField()
    is_correct = models.BooleanField()
    timestamp = djmodels.DateTimeField(null=True, blank=True)


class Event(djmodels.Model):
    class Meta:
        ordering = ['timestamp']

    owner = djmodels.ForeignKey(to=Player, on_delete=djmodels.CASCADE, related_name='events')

    name = models.StringField()
    timestamp = djmodels.DateTimeField(null=True, blank=True)
    body = models.StringField()


def custom_export(players):
    all_fields = Event._meta.get_fields()
    field_names = [i.name for i in all_fields]
    player_fields = ['participant_code', 'age', 'gender', 'income', 'session_code', 'treatment']
    yield field_names + player_fields
    for q in Event.objects.order_by('id'):
        yield [getattr(q, f) or '' for f in field_names] + [q.owner.participant.code, q.owner.age, q.owner.gender,
                                                            q.owner.income, q.owner.session.code,
                                                            q.owner.session.config.get('display_name')]
