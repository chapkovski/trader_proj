from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Player, FinQ
from django.forms import inlineformset_factory
from django import forms
import json
from otree.api import widgets


# form for fin qs

class FinQForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        jchoices = json.loads(self.instance.choices)

        exchoices = [(i, j) for i, j in enumerate(jchoices)]

        self.fields['answer'] = forms.ChoiceField(widget=widgets.RadioSelect(attrs={'required': True}),
                                                  choices=exchoices,
                                                  required=True)


# formset for fin qs
finq_formset = inlineformset_factory(parent_model=Player,
                                     model=FinQ,
                                     fields=['answer'],
                                     extra=0,
                                     can_delete=False,
                                     form=FinQForm,
                                     )


class FinQuiz(Page):
    def get_formset(self, data=None):
        return finq_formset(instance=self.player,
                            data=data, )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.get_formset()

        return context

    def get_form(self, data=None, files=None, **kwargs):
        if data and data.get('timeout_happened'):
            return super().get_form(data, files, **kwargs)
        if not data:
            return self.get_formset()
        formset = self.get_formset(data=data)
        return formset

    def before_next_page(self):
        self.player.payoff = self.player.get_correct_quiz_questions_num() * Constants.fee_per_correct_answer


class Results(Page):
    def vars_for_template(self):
        return dict(
            chosen_round=self.participant.vars.get('chosen_round', ''),
            trading_payoff=self.participant.vars.get('trading_payoff', ''),
            correct_quiz_questions=self.player.get_correct_quiz_questions_num(),
            quiz_bonus=self.player.payoff
        )


class Q(Page):
    form_model = 'player'
    form_fields = ['gender',
                   'age',
                   'nationality',
                   'email',
                   'education',
                   'study_major',
                   'course_financial',
                   'experiment_before',
                   'trading_experience',
                   'online_trading_experience',
                   'trading_frequency',
                   'portfolio_frequency',
                   'asset_class',
                   'use_leverage',
                   'purpose',
                   'difficulty']



page_sequence = [
    FinQuiz,
    Q,
    Results
]
