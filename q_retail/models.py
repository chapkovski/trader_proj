from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from django_countries.fields import CountryField

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'q'
    players_per_group = None
    num_rounds = 1
    GENDER_CHOICES = ['Male', 'Female', 'Other']
    EDUCATION_CHOICES = ['did not graduate high school',
                         'high-school graduate',
                         'undergraduate: 1st year',
                         'undergraduate: 2nd year',
                         'undergraduate: 3d year',
                         'undergraduate: 4th year',
                         'master',
                         'MBA',
                         'PhD'
                         ]
    STUDY_MAJOR_CHOICES = ['Finance', 'Economics', 'Other Management', 'Other']
    TRADING_FREQUENCY=["Multiple times a day","Daily","Weekly","Monthly","Less than once a month"]
    PORTFOLIO_FREQUENCY = ["Multiple times a day", "Daily", "Weekly", "Monthly", "Less than once a month"]
    ASSET_CLASS=["Stocks","Bonds","Derivatives (Options, Futures)","Cryptocurrencies"]
    USE_LEVERAGE=["Yes","No","Do not know"]




class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gender = models.StringField(choices=Constants.GENDER_CHOICES, widget=widgets.RadioSelectHorizontal)
    age = models.IntegerField()
    email=models.LongStringField(label='E-mail address: ',default='')
    nationality = CountryField(blank_label='(select country)',default='CA')
    education = models.StringField(choices=Constants.EDUCATION_CHOICES)
    study_major = models.StringField(choices=Constants.STUDY_MAJOR_CHOICES, label='Study major')
    course_financial = models.BooleanField(label='Did you take any course focused on financial markets')
    experiment_before = models.BooleanField(label='Have you been part of an experiment before?')
    trading_experience = models.BooleanField(label='Do you have any trading experience?')
    online_trading_experience = models.BooleanField(label='Do you use mobile trading apps?')
    trading_frequency = models.StringField(choices=Constants.TRADING_FREQUENCY,
                                   label='How often do you trade online?')
    portfolio_frequency = models.StringField(choices=Constants.PORTFOLIO_FREQUENCY,
                                   label='How often do you check the value of your portfolio?')
    asset_class = models.StringField(choices=Constants.ASSET_CLASS,
                                   label='Which asset class do you trade the most?')
    use_leverage = models.StringField(choices=Constants.USE_LEVERAGE,
                                   label='Do you use leverage (e.g., trading on margin)?')

    # Feedback questions
    purpose=models.LongStringField(label='What do you think is the purpose of this study?',default='')
    difficulty=models.LongStringField(label='Did you encounter any difficulty throughout the experiment?',default='')





