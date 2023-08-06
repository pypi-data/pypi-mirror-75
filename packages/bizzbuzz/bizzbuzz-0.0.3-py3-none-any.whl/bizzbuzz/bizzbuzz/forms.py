from django import forms
from bizzbuzz.models import Preferences

class PrefForm(forms.Form):
    class Meta:
        model = Preferences
        fields = ('apple', 'google', 'facebook', 'microsoft', 'amazon', 'samsung', 'ibm', 'twitter', 'netflix',
                  'oracle', 'sap', 'salesforce', 'tesla', 'spacex')