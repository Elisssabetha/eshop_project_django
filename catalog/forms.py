from django import forms

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_actual':
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    forbidden_words = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар')
    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'preview', 'price')

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']

        if any(word in cleaned_data.lower() for word in self.forbidden_words):
            raise forms.ValidationError('Запрещенное слово в названии')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        if any(word in cleaned_data.lower() for word in self.forbidden_words):
            raise forms.ValidationError('Запрещенное слово в описании')
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

