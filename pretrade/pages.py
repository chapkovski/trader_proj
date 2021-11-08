from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from trader_wrapper.config import Params


class GeneralPage(Page):
    def vars_for_template(self):
        return dict(gps=Params)

class CQPage(GeneralPage):
    form_model = 'player'
    form_fields = ['cq1', 'cq2', 'cq3', 'cq4']

class Instructions(GeneralPage):
    pass

page_sequence = [
    Instructions,
    CQPage]
