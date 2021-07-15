from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage



class CQPage(Page):
     form_model = 'player'
     form_fields = ['cq1','cq2','cq3','cq4']

class Instructions(Page):
     pass



page_sequence = [Instructions, CQPage]
