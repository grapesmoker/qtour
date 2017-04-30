import django.forms as forms

from django.forms import Form, ModelForm
from django.forms.widgets import DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Fieldset, Div, HTML

from core.models import *


class Html5DateInput(DateInput):

    input_type = 'date'


class TournamentForm(ModelForm):

    class Meta:
        model = Tournament
        fields = ['name', 'date', 'base_fee']

    def __init__(self, *args, **kwargs):

        if 'mode' in kwargs:
            mode = kwargs.pop('mode')
            if mode is not None:
                if mode == 'edit':
                    pass
        if 'instance' in kwargs:
            self.model = kwargs['instance']
            self.sites = self.model.tournamentsite_set.all()
            self.site_html = '<ul>'
            for site in self.sites:
                self.site_html += '<li>{}</li>'.format(site.name)
            self.site_html += '</ul>'
            #self.site_list = HTML(site_html)
        else:
            self.model = None

        super(TournamentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'new-tournament-form'
        self.helper.form_method = 'post'
        self.helper.form_action = '/create_tournament/'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'

        self.helper.layout = Layout(
            Fieldset(
                'Tournament details',
                Field('name'),
                Field('base_fee'),
                Field('date'),
                HTML(self.site_html)
            )
        )

        self.helper.add_input(Submit('submit', 'Submit'))
        self.fields['date'].widget = Html5DateInput()