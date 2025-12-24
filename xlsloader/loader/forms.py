from django import forms
from django.core.validators import FileExtensionValidator


class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(
        label='Выберите Excel файл',
        max_length=None,
        validators=[
            FileExtensionValidator(allowed_extensions=['xls', 'xlsx'])
        ]
    )
