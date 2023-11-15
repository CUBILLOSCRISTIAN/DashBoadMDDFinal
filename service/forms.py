from django import forms


class FormPrediction(forms.Form):
    lugar = forms.ChoiceField(label='Lugar de predicción')
    velocidad = forms.FloatField(label='Velocidad inicial')

    def __init__(self, lugares, *args, **kwargs):
        super(FormPrediction, self).__init__(*args, **kwargs)
        self.fields['lugar'] = forms.ChoiceField(
            label='Lugar de predicción', 
            choices=lugares
        )