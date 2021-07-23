from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants



class Trader(Page):
    live_method = 'register_event'

    def game_params(self):
        # todo: doesn't make sense to just retrieve all that from constants directlY?
        return dict(gamified=self.session.config.get('gamified', False),
                    day_params=Constants.day_params,
                    endowment=Constants.endowment,
                    dayLength=Constants.day_length_in_seconds,
                    tickFrequency=Constants.tick_frequency_in_secs,
                    numTicks=Constants.num_ticks,
                    bonusProbabilityCoef=Constants.bonus_probability_coef,
                    numStocksInBonus=Constants.num_stocks_in_bonus
                    )

    def before_next_page(self):
        self.player.set_payoffs()



page_sequence = [

    Trader,

]
