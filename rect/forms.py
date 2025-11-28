from django import forms
from .models import RectangularNotchReading

class ReadingForm(forms.ModelForm):
    class Meta:
        model = RectangularNotchReading
        fields = ['ho', 'h', 'volume', 'time']  # Match model field names
        widgets = {
            'ho': forms.NumberInput(attrs={'step': '0.001', 'class': 'form-control'}),
            'h': forms.NumberInput(attrs={'step': '0.001', 'class': 'form-control'}),
            'volume': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
            'time': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        ho = cleaned_data.get('ho')
        h = cleaned_data.get('h')
        if h <= ho:
            raise forms.ValidationError("Water surface elevation must be greater than datum height")


class MultiReadingForm(forms.Form):
    """
    A form to handle multiple readings dynamically.
    """
    num_readings = forms.IntegerField(
        min_value=4,
        max_value=7,
        initial=4,
        widget=forms.Select(
            choices=[(i, i) for i in range(4, 8)],
            attrs={'class': 'form-select'}
        )
    )
    readings = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )