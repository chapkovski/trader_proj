from django.core.management.base import BaseCommand
import logging
from trader_wrapper.models import Event, Constants, AttrDict
from dateparser import parse
from dateutil.relativedelta import relativedelta
import random
from itertools import cycle

logger = logging.getLogger(__name__)

STOCKS = ['A', 'B']
TABS = ['Trade', 'Work']


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
