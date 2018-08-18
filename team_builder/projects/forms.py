from django import forms
from django.forms import formset_factory

from . import models


class ProjectForm(forms.ModelForm):

    title = forms.CharField(
        label='Project Title',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Project Title'})
    )
    description = forms.CharField(
        label='Project Description',
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Project description',
                'rows': 5,
                'style': 'resize: both; overflow: auto;',
            }
        )
    )
    requirements = forms.CharField(
        label='Applicant Requirements',
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 5,
            }
        )
    )
    timeline = forms.CharField(
        label='Project Timeline',
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Time estimate',
                'rows': 5,
            }
        )
    )

    class Meta:
        fields = ("title", "description", "requirements", "timeline")
        model = models.Project


class PositionForm(forms.ModelForm):

    title = forms.CharField(
        label='Position Title',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Position Title'})
    )
    description = forms.CharField(
        label='Position Description',
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Position description',
                'rows': 5,
                'style': 'resize: both; overflow: auto;',
            }
        )
    )

    class Meta:
        fields = ("title", "description")
        model = models.Position


PositionFormSet = formset_factory(PositionForm, extra=1)
