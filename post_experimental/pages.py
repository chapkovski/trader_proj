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



class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [FinQuiz, ]
