from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from . import forms
from . import models


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    model = models.Profile
    template_name = "profiles/profile.html"

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['profile'] = self.get_object()
        context['active_projects'] = self.get_object().user.project.filter(completed=False)
        context['past_projects'] = self.get_object().user.project.filter(completed=True)
        return context


class ProfileEditView(LoginRequiredMixin, generic.UpdateView):
    model = models.Profile
    template_name = "profiles/profile_edit.html"
    form_class = forms.ProfileUpdateForm

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ProfileEditView, self).get_context_data(**kwargs)
        context['active_projects'] = self.get_object().user.project.filter(completed=False)
        context['past_projects'] = self.get_object().user.project.filter(completed=True)
        return context


    def get_success_url(self):
        if self.request.FILES:
            return HttpResponseRedirect(reverse("profiles:edit-profile"))
        return HttpResponseRedirect(reverse("profiles:view-profile", kwargs={'pk': self.get_object().pk}))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        profile_form = self.form_class(
            data=request.POST,
            instance=request.user.profile,
            files=request.FILES
        )
        skills_formset = forms.SkillFormSet(request.POST, request.FILES)
        if profile_form.is_valid() and skills_formset.is_valid():
            profile = profile_form.save(commit=False)
            profile.skills.clear()
            for form in skills_formset:
                skill_name = form.cleaned_data.get('skill')
                if skill_name:
                    skill = models.Skill.objects.get_or_create(skill=skill_name)[0]
                    profile.skills.add(skill)
            profile.save()
            messages.add_message(self.request, messages.SUCCESS, "Profile updated successfully!")
            return self.get_success_url()
        messages.add_message(self.request, messages.ERROR, "Something went wrong! Please check fields with errors...")
        return self.render_to_response(self.get_context_data(profile_form=profile_form, skills_formset=skills_formset))

    def get(self, request, *args, **kwargs):
        super(ProfileEditView, self).get(request, *args, **kwargs)
        profile_form = self.form_class(instance=request.user.profile)
        skills = request.user.profile.skills.all()
        skill_data = [{'skill': skill.skill} for skill in skills]
        if not skill_data:
            skills_formset = forms.SkillFormSet(initial=[{'skill': ''}])
        else:
            skills_formset = forms.SkillFormSet(initial=skill_data)
        return self.render_to_response(self.get_context_data(profile_form=profile_form, skills_formset=skills_formset))


class NotificationsView(generic.ListView):
    template_name = "profiles/notifications.html"

    def get_queryset(self):
        return models.Notification.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(NotificationsView, self).get_context_data(**kwargs)
        context['profile'] = models.Profile.objects.get(user=self.request.user)
        context['new_notifications'] = self.get_queryset().filter(read=False).order_by('-created_at')
        context['old_notifications'] = self.get_queryset().filter(read=True).order_by('-created_at')
        return context


class NotificationReadView(generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        notification = models.Notification.objects.get(pk=self.kwargs.get('pk'))
        notification.read = True
        notification.save()
        return reverse_lazy('profiles:notifications')


class NotificationDeleteView(generic.DeleteView):
    model = models.Notification
    success_url = reverse_lazy('profiles:notifications')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)