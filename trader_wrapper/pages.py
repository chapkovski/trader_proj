from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants



class Trader(Page):
    live_method = 'register_event'

    def game_params(self):
        return dict(gamified=self.session.config.get('gamified', False),
                    day_params=Constants.day_params,
                    endowment=Constants.endowment,
                    dayLength=Constants.day_length_in_seconds,
                    tickFrequency=Constants.tick_frequency_in_secs,
                    numTicks=Constants.num_ticks,
                    )

    def before_next_page(self):
        self.player.set_payoffs()



page_sequence = [

    Trader,

]
