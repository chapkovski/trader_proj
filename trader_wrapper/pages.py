from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

from pretrade.models import general_params
from pretrade.pages import GeneralPage







class AnnounceTrader(GeneralPage):
    pass

class Trader(GeneralPage):
    live_method = 'register_event'
    form_model = 'player'
    form_fields = ['exit_price']


    def before_next_page(self):
        self.player.set_payoffs()


page_sequence = [
    AnnounceTrader,
    Trader,
]
