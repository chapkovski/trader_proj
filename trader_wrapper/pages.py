from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

from pretrade.models import general_params
from pretrade.pages import GeneralPage


class PreTrade1(Page):
    def is_displayed(self):
        return self.round_number == 1


class PreTrade2(Page):
    def is_displayed(self):
        return self.round_number == 2

class BestTrader(Page):
    def is_displayed(self):
        return self.player.gamified


class Trader(GeneralPage):
    live_method = 'register_event'

    def game_params(self):
        return general_params(self.player)

    def before_next_page(self):
        self.player.set_payoffs()


page_sequence = [
    PreTrade1,
    PreTrade2,
    BestTrader,
    Trader,
]
