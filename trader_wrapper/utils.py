from django.core.management.base import BaseCommand
import logging
from trader_wrapper.models import Event, Constants, AttrDict, Player
from dateparser import parse
from dateutil.relativedelta import relativedelta
import random
from itertools import cycle
from enum import Enum


class Direction(int, Enum):
    buy = 1
    sell = -1


logger = logging.getLogger(__name__)

import pandas as pd
import numpy as np


# creating_events(p)
# p.age = random.randint(18, 100)
# p.gender = random.choice(['Male', 'Female'])
# p.income = random.randint(0, 7)
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
        self.current_timestamp = timestamp
        attainable_tasks = self.attainable_events[self.owner.current_tab]
        ev = random.choice(attainable_tasks)
        params = getattr(self, ev)()
        # this if condition is only valid for transactions (which can be unattainable due to monetary/depository reasons
        if params:
            self.register_event(event_name=ev, params=params)

    def register_event(self, event_name, params, ):
        data = dict(event_name=event_name,
                    params=params,
                    timestamp=self.current_timestamp)
        self.owner.register_event(data=data)

    def change_tab(self):
        tab = [t for t in Constants.tabs if t != self.player.current_tab][0]
        return dict(tab_name=tab)

    def transaction(self):
        o = self.owner
        stonks = o.deposit.all()
        direction = random.choice([Direction.buy, Direction.sell])
        if direction == Direction.sell:
            stonks = stonks.filter(quantity__gt=0)
            # we have nothing to sell - action impossible :( :
            if not stonks.exists():
                return
            r = random.choice(stonks)
            q = random.randrange(1, r.quantity) * direction

        if direction == Direction.buy:
            b = o.balance
            r = random.choice(stonks)
            p = o.get_price(name=r.name)
            max_q = b // p
            if max_q < 1:
                return
            q = random.randrange(1, max_q) * direction
        return dict(quantity=q, name=r.name)



    def submit_task(self):
        pass

    def change_stock_tab(self):
        current_tab = self.owner.current_stock_shown
        n = [i for i in Constants.stocks if i!=current_tab]
        return dict(tab_name=n)







class TaskSubmission(AttrDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_type = Constants.EVENT_TYPES.task_submission
        self.answer = random.randint(1000, 2000)
        self.is_task_correct = random.choice([True, False])




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
