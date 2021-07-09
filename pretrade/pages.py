from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage



class CQPage(Page):
     form_model = 'player'
     form_fields = ['cq1']



page_sequence = [CQPage]
