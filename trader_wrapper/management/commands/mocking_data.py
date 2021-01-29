from django.core.management.base import BaseCommand
import logging
from trader_wrapper.models import Event, Constants, AttrDict
from dateparser import parse
from dateutil.relativedelta import relativedelta
import random

logger = logging.getLogger(__name__)

STOCKS = ['A', 'B']
TABS = ['Trade', 'Work']


class TabChange(AttrDict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_type = Constants.EVENT_TYPES.tab_change
        self.tab_name = random.choice(TABS)


class Transaction(AttrDict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stock = random.choice(STOCKS)
        self.price = random.random()
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_type = Constants.EVENT_TYPES.price_update
        self.stock = random.choice(STOCKS)
        self.price = random.random()


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        logger.info(f'Gonna generate a lot of mocked data in trading platform')
        start_date_str = '2021-29-01 5:11pm MSK'
        start_date = parse(start_date_str)
        TASKS_FOR_RANDOM = [v for k, v in Constants.EVENT_TYPES.items() if k != 'price_update']
        length_in_sec = 600
        prob_to_gen = 0.4
        freq_price_update = 5

        for i in range(length_in_sec):
            new_date = start_date + relativedelta(seconds=i)
            new_ev = None

            if i % freq_price_update == 0:
                new_ev = PriceUpdate()

            else:
                to_do = random.random() < prob_to_gen
                if to_do:
                    what_to_do = random.choice(TASKS_FOR_RANDOM)
                    if what_to_do == Constants.EVENT_TYPES.tab_change:
                        new_ev = TabChange()

                    elif what_to_do == Constants.EVENT_TYPES.task_submission:
                        new_ev = TaskSubmission()
                    elif what_to_do == Constants.EVENT_TYPES.transaction:
                        new_ev = Transaction()
            if new_ev:
                a = Event.objects.create(**new_ev, timestamp=new_date)
                print(a, new_ev)
        print("JOPPA MIRA", Event.objects.count())
