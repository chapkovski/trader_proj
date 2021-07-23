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
    EDUCATION_CHOICES = ['high-school graduate',
                         'undergraduate: 1st year',
                         'undergraduate: 2nd year',
                         'undergraduate: 3d year',
                         'undergraduate: 4th year',
                         'master',
                         'MBA',
                         'PhD'
                         ]
    STUDY_MAJOR_CHOICES = ['Finance', 'Economics', 'Other Management', 'Other']
    COURSE_FINANCIAL_CHOICES = ['No', 'Yes, one', 'Yes, two', 'Yes, three or more']

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
    gender = models.StringField(choices=Constants.GENDER_CHOICES, widget=widgets.RadioSelectHorizontal,
                                label='What is your gender?')
    age = models.IntegerField(label='How old are you?')
    nationality = CountryField(verbose_name='What is your nationality?', null=True, blank=False )
    education = models.StringField(choices=Constants.EDUCATION_CHOICES)
    study_major = models.StringField(choices=Constants.STUDY_MAJOR_CHOICES, label='Study major')
    experiment_before = models.BooleanField(label='Have you been part of an experiment before?')
    trading_experience = models.BooleanField(label='Do you have any trading experience?')
    course_financial = models.StringField(choices=Constants.COURSE_FINANCIAL_CHOICES,
                                          label='Did you take any course focused on financial markets')
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
