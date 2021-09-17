from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

from pretrade.models import general_params
from pretrade.pages import GeneralPage






from pprint import pprint
class Trader(GeneralPage):
    live_method = 'register_event'

    def game_params(self):
        gp = general_params(self.player)
        return gp

    def before_next_page(self):
        self.player.set_payoffs()


page_sequence = [

    Trader,
]
