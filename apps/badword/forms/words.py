from django import forms

from apps.badword.models import Word


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ["word"]
