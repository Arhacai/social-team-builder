from django import forms
from django.core.validators import MaxLengthValidator
from django.forms import formset_factory

from . import models


class ProfileUpdateForm(forms.ModelForm):

    display_name = forms.CharField(
        label='Display Name',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter your desired display name...'}),
    validators = [MaxLengthValidator]
    )
    bio = forms.CharField(
        label='About You',
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Tell us about yourself...',
                'style': 'resize: both; overflow: auto;',
            }
        ),
        validators=[MaxLengthValidator]
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput
    )

    class Meta:
        fields = ("display_name", "bio", "avatar",)
        model = models.Profile


class SkillUpdateForm(forms.ModelForm):
    skill = forms.CharField(
        label='Skill',
        widget=forms.TextInput(
            attrs={'placeholder': 'Skill'}),
        required=False,
        validators=[MaxLengthValidator]
    )

    class Meta:
        model = models.Skill
        fields = ("skill",)


SkillFormSet = formset_factory(SkillUpdateForm, extra=0)
