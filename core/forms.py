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
            self.mode = kwargs.pop('mode')
        else:
            self.mode = 'view'

        if 'tour_id' in kwargs:
            self.tour_id = kwargs.pop('tour_id')
        else:
            self.tour_id = None

        if 'instance' in kwargs:
            self.model = kwargs['instance']
            self.tour_id = self.model.id
        elif self.tour_id is not None:
            self.model = Tournament.objects.get(id=self.tour_id)
        else:
            self.model = None

        if self.model is not None:
            self.sites = self.model.tournamentsite_set.all()
            self.site_html = '<div class="form-group">'
            self.site_html += '<label class="control-label col-sm-2">Sites</label>'
            self.site_html += '<div class="col-sm-10 controls">'
            for site in self.sites:
                self.site_html += '<p><a href="/site/{}">{}</a></p>'.format(site.id, site.site_name)
            if self.mode == 'edit':
                self.site_html += '<a href="/add_site/{}" class="btn btn-default">Add site</a>'.format(self.model.id)
            self.site_html += '</div></div>'
        else:
            self.model = None
            self.site_html = ''

        super(TournamentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'new-tournament-form'
        self.helper.form_method = 'post'
        if self.mode == 'add':
            self.helper.form_action = '/create_tournament/'
        elif self.mode == 'edit' and self.tour_id is not None:
            self.helper.form_action = '/tournament/{}/'.format(self.tour_id)

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

        if self.mode == 'add' or self.mode == 'edit':
            self.helper.add_input(Submit('submit', 'Submit'))

        self.fields['date'].widget = Html5DateInput()
        if self.mode == 'view':
            for key in self.fields.keys():
                self.fields[key].widget.attrs['disabled'] = True


class TournamentSiteForm(ModelForm):

    class Meta:
        model = TournamentSite
        fields = ['site_name','address', 'city', 'state', 'zip', 'country']

    def __init__(self, *args, **kwargs):

        if 'tour_id' in kwargs:
            self.tour_id = kwargs.pop('tour_id')
        else:
            raise ValueError('Must provide tournament id!')

        if 'mode' in kwargs:
            self.mode = kwargs.pop('mode')
        else:
            self.mode = 'view'

        self.model = kwargs.get('instance', None)

        super(TournamentSiteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'new-site-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        if self.mode == 'add':
            self.helper.form_action = '/add_site/{}/'.format(self.tour_id)
        elif self.mode == 'edit' and self.model is not None:
            self.helper.form_action = '/site/{}/'.format(self.model.id)
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'

        tour = Tournament.objects.get(id=self.tour_id)
        self.fields['tournament'] = forms.ChoiceField(choices=((tour.id, tour.name), ))

        if self.mode == 'add':
            self.helper.add_input(Submit('submit', 'Add site'))
        elif self.mode == 'edit':
            self.helper.add_input(Submit('submit', 'Submit'))
        elif self.mode == 'view':
            for key in self.fields.keys():
                self.fields[key].widget.attrs['disabled'] = True