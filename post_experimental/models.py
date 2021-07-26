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
import json
from django.db import models as djmodels
from django.db.models import F
from pprint import pprint
import yaml
from django_countries.fields import CountryField

author = 'Philipp Chapkovski, HSE Moscow, chapkovski@gmail.com'

doc = """
Post experimental questionnaire including financial quiz
"""


class Constants(BaseConstants):
    name_in_url = 'post_experimental'
    players_per_group = None
    num_rounds = 1
    fee_per_correct_answer = c(1)
    with open(r'./data/financial_quiz.yaml') as file:
        fqs = yaml.load(file, Loader=yaml.FullLoader)

    GENDER_CHOICES = ['Male', 'Female', 'Other']
    EDUCATION_CHOICES = ['did not graduate high school',
                         'high-school graduate',
                         'undergraduate: 1st year',
                         'undergraduate: 2nd year',
                         'undergraduate: 3d year',
                         'undergraduate: 4th year',
                         'master',
                         'MBA',
                         'PhD'
                         ]
    STUDY_MAJOR_CHOICES = ['Finance', 'Economics', 'Other Management', 'Other']
    TRADING_FREQUENCY = ["Multiple times a day", "Daily", "Weekly", "Monthly", "Less than once a month"]
    PORTFOLIO_FREQUENCY = ["Multiple times a day", "Daily", "Weekly", "Monthly", "Less than once a month"]
    ASSET_CLASS = ["Stocks", "Bonds", "Derivatives (Options, Futures)", "Cryptocurrencies"]
    USE_LEVERAGE = ["Yes", "No", "Do not know"]


class Subsession(BaseSubsession):
    def creating_session(self):
        cqs = []
        for p in self.get_players():
            qs = Constants.fqs.copy()

            for i in qs:
                pprint(i)
                j = i.copy()
                j['choices'] = json.dumps(i['choices'])
                cqs.append(FinQ(owner=p, **j))

        FinQ.objects.bulk_create(cqs)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gender = models.StringField(choices=Constants.GENDER_CHOICES, widget=widgets.RadioSelectHorizontal)
    age = models.IntegerField()
    email = models.LongStringField(label='E-mail address: ', default='')
    nationality = CountryField(blank_label='(select country)', default='CA')
    education = models.StringField(choices=Constants.EDUCATION_CHOICES)
    study_major = models.StringField(choices=Constants.STUDY_MAJOR_CHOICES, label='Study major')
    course_financial = models.BooleanField(label='Did you take any course focused on financial markets')
    experiment_before = models.BooleanField(label='Have you been part of an experiment before?')
    trading_experience = models.BooleanField(label='Do you have any trading experience?')
    online_trading_experience = models.BooleanField(label='Do you use mobile trading apps?')
    trading_frequency = models.StringField(choices=Constants.TRADING_FREQUENCY,
                                           label='How often do you trade online?')
    portfolio_frequency = models.StringField(choices=Constants.PORTFOLIO_FREQUENCY,
                                             label='How often do you check the value of your portfolio?')
    asset_class = models.StringField(choices=Constants.ASSET_CLASS,
                                     label='Which asset class do you trade the most?')
    use_leverage = models.StringField(choices=Constants.USE_LEVERAGE,
                                      label='Do you use leverage (e.g., trading on margin)?')

    # Feedback questions
    purpose = models.LongStringField(label='What do you think is the purpose of this study?', default='')
    difficulty = models.LongStringField(label='Did you encounter any difficulty throughout the experiment?', default='')

    def get_correct_quiz_questions_num(self):
        return self.finqs.filter(answer=F('correct')).count()



class FinQ(djmodels.Model):
    owner = djmodels.ForeignKey(to=Player, on_delete=djmodels.CASCADE, related_name='finqs')
    label = models.StringField()
    choices = models.StringField()
    correct = models.IntegerField()
    answer = models.IntegerField()


def custom_export(players):
    session = players[0].session

    player_fields = ['age', 'gender', 'income']

    for q in FinQ.objects.filter(answer__isnull=False):
        yield [q.label,
               q.answer
               ] + [q.owner.participant.code,
                    q.owner.session.code,
                    q.owner.session.config.get('display_name'),
                    ] + [
                  getattr(q.owner, f) or '' for f in player_fields
              ]
