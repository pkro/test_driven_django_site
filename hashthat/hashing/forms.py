from django import forms
import hashlib


class HashForm(forms.Form):
    choices = [(e, e) for e in hashlib.algorithms_available]
    algo = forms.ChoiceField(choices=choices, widget=forms.Select)
    text = forms.CharField(label='Enter text here:', widget=forms.Textarea)