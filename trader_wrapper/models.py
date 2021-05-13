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
    tick = 5  # how often prices are updated (in seconds)
    stocks = ['A', 'B', 'ETF_A', 'ETF_B']
    tabs = ['work', 'trade']
    default_tab = 'trade'
    endowment = 100

    num_rounds = 8
    wages = [10, 20]
    fees = [0, 1]
    wages_fees = list(product(wages, fees))
    assert num_rounds == len(wages_fees) * 2, 'Something is wrong with logic in wages/fees'
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
            p.generate_deposit()  # TODO: in production move to bulk update right here
            p.generate_prices()  # TODO: in production move to bulk update right here
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
    ########### BLOCK: post experimental survey quesitons.  ##############################################################
    # TODO: move to a separate app in production
    age = models.IntegerField()
    gender = models.StringField()
    income = models.IntegerField()

    ############ END OF: post experimental survey quesitons.  #############################################################
    def register_event(self, data):
        """That's the main manager that processes all events that arrive from frontend (and from mocking simulator)"""
        # TODO: from frontent apparentley will need to parse the date from string.
        data['source'] = SourceType.client  # I guess we can safely assume that whatever comes here is generated by fron

        self.events.create(**data)
        # TODO: we may think to move all this logic beneath to signals. It needs some thinking how
        # TODO: organize it in a smarter than this way. Right now it is ugly AF
        event_type = data.get('name')
        if event_type == EventType.transaction:
            self.update_stocks_and_balance(data)
        if event_type == EventType.task:
            self.update_tasks_and_balance(data)
        if event_type == EventType.change_stock_tab:
            self.update_current_stock_tab(data)
        if event_type == EventType.change_tab:
            self.update_current_tab(data)
        self.save()  # we only need this in mocking, but no harm in production
        # TODO - we need to return something to front here in production. No need to this for mocking data though

    def update_stocks_and_balance(self, data):
        timestamp = data.get('timestamp')
        body = data.get('body')
        direction = body.get('direction')
        quantity = body.get('quantity')
        name = body.get('name')
        stock = self.deposit.get(name=name)
        old_quantity = stock.quantity
        stock.quantity += quantity
        stock.save()
        price = self.get_price(timestamp, stock.name)
        Event.objects.create(owner=self,
                             timestamp=timestamp,
                             source=SourceType.inner,
                             name='change_in_deposit',
                             body=dict(stock_name=stock.name,
                                       direction=direction,
                                       price=price,
                                       old_quantity=old_quantity,
                                       quantity_to_process=quantity,
                                       new_quantity=stock.quantity,
                                       ))

        # we invert direction here because selling and buying affects balance in an inverted way (obviosly)
        amount = -1 * price * quantity
        old_balance = self.ending_balance
        self.ending_balance += amount

        Event.objects.create(owner=self,
                             timestamp=timestamp,
                             source=SourceType.inner,
                             name='change_in_balance',
                             balance=self.ending_balance,
                             body=dict(
                                 old_balance=old_balance,
                                 amount=amount,
                                 new_balance=self.ending_balance,
                                 source='trade'
                             ))
        if self.transaction_fee and self.transaction_fee > 0:
            # TODO: do we need that? for speed let's keep like that for a moment
            self.update_balance_and_register_fee(timestamp)
        # TODO: in production some awards (based on time spent) are given in front, not inner
        # TODO: if the award is inner-generated then we need to return something here to give info to front
        self.assign_awards(timestamp)

    def assign_awards(self, timestamp):
        n_transactions = self.events.filter(name='transaction').count()
        award = Constants.awards.get(n_transactions)
        if award:
            event = Event.objects.create(owner=self,
                                 timestamp=timestamp,
                                 source=SourceType.inner,
                                 name='award',
                                 body=award)
            return event
    def update_balance_and_register_fee(self, timestamp):
        old_balance = self.ending_balance
        self.ending_balance -= self.transaction_fee

        Event.objects.create(owner=self,
                             timestamp=timestamp,
                             source=SourceType.inner,
                             name='change_in_balance',
                             balance=self.ending_balance,
                             body=dict(
                                 old_balance=old_balance,
                                 amount=self.transaction_fee,
                                 new_balance=self.ending_balance,
                                 source='transaction_fee'
                             ))

    def update_tasks_and_balance(self, data):
        body = data.get('body')
        task_id = body.get('task_id')
        timestamp = data.get('timestamp')
        task = Task.objects.get(id=task_id)
        task.answer = body.get('answer')
        task.is_correct = task.answer == task.correct_answer
        task.save()
        self.num_tasks_submitted += 1
        self.num_correct_tasks_submitted += task.is_correct
        Event.objects.create(owner=self,
                             timestamp=timestamp,
                             name='task_submitted',
                             source=SourceType.inner,
                             body=dict(
                                 answer=task.answer,
                                 is_correct=task.is_correct,
                                 num_tasks_submitted=self.num_tasks_submitted,
                                 num_correct_tasks_submitted=self.num_correct_tasks_submitted,
                             ))

        if task.is_correct:
            price = self.wage
            amount = price * task.is_correct
            old_balance = self.ending_balance
            self.ending_balance += amount
            Event.objects.create(owner=self,
                                 timestamp=timestamp,
                                 source=SourceType.inner,
                                 name='change_in_balance',
                                 balance=self.ending_balance,
                                 body=dict(
                                     old_balance=old_balance,
                                     amount=amount,
                                     new_balance=self.ending_balance,
                                     source='work'
                                 ))
        new_task = self.get_current_task(timestamp=timestamp)
        Event.objects.create(owner=self,
                             timestamp=timestamp,
                             name='new_task_generated',
                             source=SourceType.inner,
                             body=dict(
                                 id=new_task.id,
                                 correct_answer=new_task.correct_answer
                             ))

    def update_current_stock_tab(self, data):
        new_stock_tab = data.get('tab_name')
        self.current_stock_shown = new_stock_tab

    def update_current_tab(self, data):
        new_tab = data.get('body').get('tab_name')
        self.current_tab = new_tab
        self.save()

    def get_price(self, timestamp, stock_name):
        current_prices = self.price_request(timestamp=timestamp)
        for i in current_prices:
            if i.get('name') == stock_name:
                return i.get('price')

    def generate_single_price(self, name):
        # TODO: somewhere here we inject proper price generation, right now just a random uniform
        return random.random()

    def generate_prices(self):
        """we bulk create price updates here.
        The trick is that also in production we pre-generate a flow of prices BEFORE the trading day starts
        with corresponding timestamps. Then we feed them every time we get a price_update request from a client.
        That we guarantee the fastest possible reaction.
        """

        # TODO: NB! that obviosly should be used detached from the timestamp because we don't know
        #  when the player actually arrives to the corresponding page. however for mock generating reasons
        #  it's ok to keep it like that for now.

        # TODO: all this BS should be optimized for production.
        t = self.start_time
        times = []
        while t < self.end_time:
            times.append(t)
            t = t + relativedelta(seconds=Constants.tick)
        n = len(times)
        stocks_with_prices = get_prices(Constants.stocks_with_params, n)

        ps = []
        for i in stocks_with_prices:
            for j, p in enumerate(i.get('prices')):
                t = times[j]
                ps.append(Price(price=p, timestamp=t, name=i.get('name'), owner=self))

        # TODO: we may limit quantity here with `batch_size` for sqlite (it overloads with too long queries)
        Price.objects.bulk_create(ps)
        # TODO: we seriously need to think whether we want to register these events in advance in production
        #  we can't do this tbh because we don't know exact timestamps of the starting time.
        #  That works for mocked data only.
        events = []
        for p in ps:
            events.append(Event(owner=self, source=SourceType.inner,
                                name='price_update',
                                timestamp=p.timestamp,
                                body=dict(stock_name=p.name, new_stock_price=p.price)
                                ))
        Event.objects.bulk_create(events)

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
        t = Task.objects.create(**task_body)
        return t

    def precreating_task(self, t):
        """TODO: In production returns two"""
        return dict(body='',
                    correct_answer='asdf',
                    timestamp=t,
                    owner=self)

    def price_request(self, timestamp):
        """Returns a dict of recent prices that are earlier than a given timestamp"""

        most_recent_time_stamp = self.prices.filter(timestamp__lte=timestamp).latest().timestamp
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

    def __str__(self):
        return f'Price {self.name}: price: {self.price}; timestamp: {self.timestamp}'


class Deposit(djmodels.Model):
    owner = djmodels.ForeignKey(to=Player, on_delete=djmodels.CASCADE, related_name='deposit')
    quantity = models.IntegerField()
    name = models.StringField()


class Task(djmodels.Model):
    class Meta:
        ordering = ['timestamp']
        get_latest_by = 'timestamp'

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
    source = models.StringField(doc='can be either inner (due to some internal processes) or from client')
    name = models.StringField()
    timestamp = djmodels.DateTimeField(null=True, blank=True)
    body = models.StringField()
    balance = models.FloatField()  # to store the current state of bank account


def custom_export(players):
    session = players[0].session
    all_fields = Event._meta.get_fields()
    field_names = [i.name for i in all_fields]

    player_fields = ['participant_code',
                     'round_number',
                     'trading_round_starts',
                     'trading_round_ends',
                     'age', 'gender', 'income',
                     'starting_balance',
                     'ending_balance',
                     'wage',
                     'transaction_fee',
                     'num_tasks_submitted',
                     'num_correct_tasks_submitted',
                     'session_code', 'treatment']
    yield field_names + player_fields
    for q in Event.objects.filter(owner__session=session).order_by('owner__session', 'owner__round_number',
                                                                   'timestamp'):
        yield [getattr(q, f) or '' for f in field_names] + [q.owner.participant.code,
                                                            q.owner.round_number,
                                                            q.owner.start_time,
                                                            q.owner.end_time,
                                                            q.owner.age,
                                                            q.owner.gender,
                                                            q.owner.income,
                                                            q.owner.starting_balance,
                                                            q.owner.ending_balance,
                                                            q.owner.wage,
                                                            q.owner.transaction_fee,
                                                            q.owner.num_tasks_submitted,
                                                            q.owner.num_correct_tasks_submitted,
                                                            q.owner.session.code,

                                                            q.owner.session.config.get('display_name')]
