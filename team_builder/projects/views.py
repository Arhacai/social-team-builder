from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic

from . import models
from . import forms


class ProjectView(generic.TemplateView):
    model = models.Project
    template_name = "projects/project.html"

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['project'] = self.get_object()
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Project
    template_name = 'projects/project_new.html'
    form_class = forms.ProjectForm

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        if 'project_form' not in context:
            context['project_form'] = self.form_class()
            context['position_formset'] = forms.PositionFormSet()
        return context

    def post(self, request, *args, **kwargs):
        project_form = self.form_class(request.POST)
        position_formset = forms.PositionFormSet(request.POST)
        if project_form.is_valid() and position_formset.is_valid():
            project = project_form.save(commit=False)
            project.owner = self.request.user
            project.save()
            for form in position_formset:
                position = form.save()
                project.positions.add(position)
            return HttpResponseRedirect(reverse('projects:view-project', kwargs={'pk': project.pk}))
        return self.render_to_response(self.get_context_data(project_form=project_form, position_formset=position_formset))


class ProjectEditView(LoginRequiredMixin, generic.UpdateView):
    model = models.Project
    template_name = 'projects/project_edit.html'
    form_class = forms.ProjectForm

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(ProjectEditView, self).get_context_data(**kwargs)
        if 'project_form' not in context:
            context['project_form'] = self.form_class()
            context['position_formset'] = forms.PositionFormSet()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        project_form = self.form_class(data=request.POST, instance=self.object)
        position_formset = forms.PositionFormSet(request.POST)
        if project_form.is_valid() and position_formset.is_valid():
            project = project_form.save(commit=False)
            project.positions.all().delete()
            project.save()
            for form in position_formset:
                if form.cleaned_data.get('title'):
                    position = form.save()
                    project.positions.add(position)
            messages.add_message(request, messages.SUCCESS, "Probando")
            return self.get_success_url()
        return self.render_to_response(self.get_context_data(object=self.object, project_form=project_form, position_formset=position_formset))

    def get(self, request, *args, **kwargs):
        super(ProjectEditView, self).get(request, *args, **kwargs)
        project_form = self.form_class(instance=self.object)
        positions = self.object.positions.all()
        data = [{'title': position.title, 'description': position.description} for position in positions]
        if not data:
            position_formset = forms.PositionFormSet(initial=[{'title': '', 'description': ''}])
        else:
            position_formset = forms.PositionFormSet(initial=data)
        return self.render_to_response(self.get_context_data(project_form=project_form, position_formset=position_formset))


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Project
    success_url = reverse_lazy('profiles:view-profile')


class ProjectSearchView(generic.ListView):
    template_name = "index.html"

    def get_queryset(self):
        term = self.request.GET.get('search_term')
        query_set = models.Project.objects.filter(
            Q(title__icontains=term) |
            Q(description__icontains=term)
        )
        return query_set

    def get_context_data(self, **kwargs):
        context = super(ProjectSearchView, self).get_context_data(**kwargs)
        context['active_projects'] = self.get_queryset().filter(completed=False)
        context['past_projects'] = self.get_queryset().filter(completed=True)
        context['positions'] = models.Position.objects.all()
        return context


class ProjectFilterView(generic.ListView):
    model = models.Project
    template_name = "index.html"

    def get_queryset(self):
        title = self.kwargs.get('title')
        query_set = models.Project.objects.filter(positions__title__icontains=title)
        return query_set

    def get_context_data(self, **kwargs):
        context = super(ProjectFilterView, self).get_context_data(**kwargs)
        context['active_projects'] = self.get_queryset().filter(completed=False)
        context['past_projects'] = self.get_queryset().filter(completed=True)
        context['positions'] = models.Position.objects.all()
        context['selected'] = self.kwargs.get('title')
        return context


class ProjectChangeStatusView(generic.RedirectView):

    query_string = True
    pattern_name = 'projects:view-project'

    def get_redirect_url(self, *args, **kwargs):
        project = get_object_or_404(models.Project, pk=kwargs.get('pk'))
        if project.completed:
            project.completed = False
        else:
            project.completed = True
        project.save()
        return super(ProjectChangeStatusView, self).get_redirect_url(*args, **kwargs)
