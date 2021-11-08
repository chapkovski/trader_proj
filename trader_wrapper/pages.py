from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from .config import Params
from pretrade.pages import GeneralPage







class AnnounceTrader(GeneralPage):
    pass

class Trader(GeneralPage):
    live_method = 'register_event'
    form_model = 'player'
    form_fields = ['exit_price']
    def vars_for_template(self):
        return dict(gps=Params)

    def before_next_page(self):
        self.player.set_payoffs()


page_sequence = [
    AnnounceTrader,
    Trader,
]
