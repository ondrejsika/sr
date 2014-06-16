from django import forms

from .models import GirlRank, Girl


class RateForm(forms.ModelForm):
    class Meta:
        model = GirlRank
        fields = ('rank', )

    def __init__(self, girl, user, *args, **kwargs):
        super(RateForm, self).__init__(*args, **kwargs)

        self.girl = girl
        self.user = user

    def save(self, commit=True):
        obj = super(RateForm, self).save(commit=False)
        obj.user = self.user
        obj.girl = self.girl
        if commit:
            obj.save()
        return obj


class GirlForm(forms.ModelForm):
    class Meta:
        model = Girl
        exclude = ('nominated_by', )

    def __init__(self, user, *args, **kwargs):
        super(GirlForm, self).__init__(*args, **kwargs)

        self.user = user

    def save(self, commit=True):
        obj = super(GirlForm, self).save(commit=False)
        obj.nominated_by = self.user
        if commit:
            obj.save()
        return obj

