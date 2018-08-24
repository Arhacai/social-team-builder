from django import forms
from django.core.validators import MaxLengthValidator
from django.forms import formset_factory

from profiles.models import Skill
from . import models


class ProjectForm(forms.ModelForm):

    title = forms.CharField(
        label='Project Title',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Project Title'}),
        validators=[MaxLengthValidator]
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
        ),
        validators=[MaxLengthValidator]
    )
    requirements = forms.CharField(
        label='Applicant Requirements',
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 5,
            }
        ),
        validators=[MaxLengthValidator]
    )
    timeline = forms.CharField(
        label='Project Timeline',
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Time estimate',
                'rows': 5,
            }
        ),
        validators=[MaxLengthValidator]
    )

    class Meta:
        fields = ("title", "description", "requirements", "timeline")
        model = models.Project


class PositionForm(forms.ModelForm):

    title = forms.CharField(
        label='Position Title',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Position Title'}),
        validators=[MaxLengthValidator]
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
        ),
        validators=[MaxLengthValidator]
    )
    related_skill = forms.CharField(
        label='Related Skill',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Related Skill'}),
        validators=[MaxLengthValidator]
    )

    def clean_related_skill(self):
        related_skill = self.cleaned_data.get('related_skill')
        skill, _ = Skill.objects.get_or_create(skill=related_skill)
        return skill


    class Meta:
        fields = ("title", "description", "related_skill")
        model = models.Position


PositionFormSet = formset_factory(PositionForm, extra=1)
