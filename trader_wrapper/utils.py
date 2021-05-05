from django.core.management.base import BaseCommand
import logging
from trader_wrapper.models import Event, Constants, AttrDict, Player
from dateparser import parse
from dateutil.relativedelta import relativedelta
import random
from itertools import cycle

logger = logging.getLogger(__name__)

STOCKS = ['A', 'B']
TABS = ['Trade', 'Work']

import pandas as pd
import numpy as np

creating_events(p)
p.age = random.randint(18, 100)
p.gender = random.choice(['Male', 'Female'])
p.income = random.randint(0, 7)
def pp(start, end, n):
    """Taken from: https://stackoverflow.com/questions/50559078/generating-random-dates-within-a-given-range-in-pandas.
    Just generate a sorted list of N random timestamps between two dates from two python datetimes"""
    start_u = pd.Timestamp(start).value // 10 ** 9
    end_u = pd.Timestamp(end).value // 10 ** 9
    return sorted(pd.to_datetime(
        pd.DatetimeIndex((10 ** 9 * np.random.randint(start_u, end_u, n, dtype=np.int64)).view('M8[ns]'))))


class MockPlayer:
    attainable_events = dict(
        work=['submit_task', 'change_tab'],
        trade=['change_tab', 'transaction', 'change_stock_tab']
    )

    def __init__(self, owner, num_events):
        self.owner = owner
        self.num_events = num_events
        start = self.owner.start_time
        end = self.owner.end_time
        event_timestamps = pp(start, end, num_events)
        for i in event_timestamps:
            self.generate_random_event(i)

    def generate_random_event(self, timestamp):

    def register_event(self, event_name, params, ):
        pass

    def change_tab(self):
        tab = [t for t in self.tabs if t != self.player.current_tab][0]
        self.register_event(event_name='change_tab', params={'tab': tab})

    def transaction(self):
        self.stock = stock
        self.price = price
        self.event_type = Constants.EVENT_TYPES.transaction
        self.quantity = random.randint(0, 100)
        self.total_amount = self.quantity * self.price


class TabChange(AttrDict):

    def __init__(self, tab, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_type = Constants.EVENT_TYPES.tab_change
        self.tab_name = tab


class Transaction(AttrDict):
    def __init__(self, price, stock, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stock = stock
        self.price = price
        self.event_type = Constants.EVENT_TYPES.transaction
        self.quantity = random.randint(0, 100)
        self.total_amount = self.quantity * self.price


class TaskSubmission(AttrDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_type = Constants.EVENT_TYPES.task_submission
        self.answer = random.randint(1000, 2000)
        self.is_task_correct = random.choice([True, False])


class PriceUpdate(AttrDict):
    def __init__(self, stock, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_type = Constants.EVENT_TYPES.price_update
        self.stock = stock
        self.price = random.random()


def creating_events(owner):
    logger.info(f'Gonna generate a lot of mocked data in trading platform')
    start_date_str = '2021-29-01 5:11pm MSK'
    start_date = parse(start_date_str)
    TASKS_FOR_RANDOM = [v for k, v in Constants.EVENT_TYPES.items() if k != 'price_update']
    length_in_sec = 600
    prob_to_gen = 0.4
    freq_price_update = 5
    cur_price = dict(A=0, B=0)
    events_to_create = []
    tabs_cycle = cycle(TABS)
    current_tab = next(tabs_cycle)
    for i in range(length_in_sec):
        new_date = start_date + relativedelta(seconds=i)
        new_ev = None

        if i % freq_price_update == 0:
            for s in STOCKS:
                new_ev = PriceUpdate(stock=s)
                cur_price[s] = new_ev.price
                ev = Event(**new_ev, timestamp=new_date, owner=owner)
                print(new_ev)
                events_to_create.append(ev)

            continue


        else:
            to_do = random.random() < prob_to_gen
            if to_do:
                what_to_do = random.choice(TASKS_FOR_RANDOM)
                if what_to_do == Constants.EVENT_TYPES.tab_change:
                    current_tab = next(tabs_cycle)
                    new_ev = TabChange(tab=current_tab)
                elif what_to_do == Constants.EVENT_TYPES.task_submission:
                    new_ev = TaskSubmission()
                elif what_to_do == Constants.EVENT_TYPES.transaction:
                    stock = random.choice(STOCKS)
                    new_ev = Transaction(price=cur_price[stock], stock=stock)
        if new_ev:
            ev = Event(**new_ev, timestamp=new_date, owner=owner)
            print(new_ev)
            events_to_create.append(ev)
    Event.objects.bulk_create(events_to_create)
