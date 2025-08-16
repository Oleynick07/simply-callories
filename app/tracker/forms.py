from django import forms
from .models import ConsumptionEntry


class ConsumptionEntryForm(forms.ModelForm):
    class Meta:
        model = ConsumptionEntry
        fields = ['name', 'calories', 'date', 'quantity_g']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
        self.fields['calories'].widget.attrs['placeholder'] = 'kcal'
        self.fields['quantity_g'].widget.attrs['placeholder'] = 'grams (optional)'

