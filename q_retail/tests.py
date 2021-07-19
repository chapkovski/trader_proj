from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random
from django_countries import Countries


class PlayerBot(Bot):
    def play_round(self):
        c = list(Countries().alt_codes)
        answer = {'gender': random.choice(Constants.GENDER_CHOICES),
                  'age': random.randint(0, 100),
                  'nationality': random.choice(c),
                  'education': random.choice(Constants.EDUCATION_CHOICES),
                  'study_major': random.choice(Constants.STUDY_MAJOR_CHOICES),
                  'experiment_before': random.choice([False, True]),
                  'trading_experience': random.choice([False, True]),
                  'course_financial': random.choice(Constants.COURSE_FINANCIAL_CHOICES),
                  'email': 'bot@mail.com',
                  'purpose': 'Nothing',
                  'strategy': 'Random',
                  'speedbump': 'Should I have?',
                  'difficulty': 'So hard!'

                  }
                  

        yield pages.Q, answer
