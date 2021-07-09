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
from pprint import pprint
import yaml
author = 'Philipp Chapkovski, HSE Moscow, chapkovski@gmail.com'

doc = """
Post experimental questionnaire including financial quiz
"""



class Constants(BaseConstants):
    name_in_url = 'post_experimental'
    players_per_group = None
    num_rounds = 1
    with open(r'./data/financial_quiz.yaml') as file:
        fqs = yaml.load(file, Loader=yaml.FullLoader)


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
    age = models.IntegerField()
    gender = models.StringField()
    income = models.IntegerField()


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
