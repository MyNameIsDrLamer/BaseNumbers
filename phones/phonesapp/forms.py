from .models import Numbers, Files
from django.forms import ModelForm, FileInput, Select, TextInput, Textarea, CheckboxInput, DateInput


class NumbersForm(ModelForm):
    class Meta:
        model = Numbers
        fields = ['number', 'attachment', 'comment', 'date_attach', 'cf']
        widgets = {
            'number': TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
            'attachment': Select(attrs={'class': 'form-select', 'style': 'width: 300px;'}),
            'comment': Textarea(attrs={'class': 'form-control', 'style': 'width: 500px; resize: none;', 'cols': '50',
                                       'rows': '5'}),
            'date_attach': DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'style': 'width: 300px;', 'id': 'datepicker'}),
            'cf': CheckboxInput,
        }


class AddFiles(ModelForm):
    class Meta:
        model = Files
        fields = ['file', 'provider']
        widgets = {
            'file': FileInput(attrs={'class': 'form-control', 'style': 'width: 350px'}),
            'provider': Select(attrs={'type:': 'file', 'class': 'form-select', 'style': 'width: 350px;'})
        }