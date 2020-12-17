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
    pass


class Results(Page):
    pass


page_sequence = [
    Intro,
    TraderInstructions,
    TraderExample1,
    TraderExample2,
    RETInstructions,
    ComprehensionCheck,
    Video,
    VideoQuiz,
    Trader,
    Results,
]
