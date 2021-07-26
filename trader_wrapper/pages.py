from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

from pretrade.models import general_params
from pretrade.pages import GeneralPage


class Trader(GeneralPage):
    live_method = 'register_event'

    def game_params(self):
        return general_params(self.subsession)

    def before_next_page(self):
        self.player.set_payoffs()


page_sequence = [
    Trader,
]
