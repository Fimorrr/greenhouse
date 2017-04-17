from django import forms
from .models import Plant

class SevForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SevForm, self).__init__(*args, **kwargs)
        plant_choices = [(i['id'], i['name']) for i in Plant.objects.values('id', 'name').distinct()]
        plant = forms.ChoiceField(choices=plant_choices)
        self.fields["plant"] = plant