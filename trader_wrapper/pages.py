from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Intro(Page):
    pass


class TraderInstructions(Page):
    pass


class TraderExample1(Page):
    pass


class TraderExample2(Page):
    pass


class RETInstructions(Page):
    pass


class ComprehensionCheck(Page):
    pass


class Video(Page):
    pass


class VideoQuiz(Page):
    pass


class Trader(Page):
    live_method = 'register_event'

    def game_params(self):
        return dict(gamified=self.session.config.get('gamified', False),
                    day_params=Constants.day_params,
                    endowment=Constants.endowment)

    def post(self):
        # TODO: we inject some extra params here. (not sure we need it though since we 'll get most of the data via channels
        print('JOPA', self.request.POST)
        return super().post()


class Results(Page):
    pass


page_sequence = [
    # Intro,
    # TraderInstructions,
    # TraderExample1,
    # TraderExample2,
    # RETInstructions,
    # ComprehensionCheck,
    # Video,
    # VideoQuiz,
    Trader,
    # Results,
]
