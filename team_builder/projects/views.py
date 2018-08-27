from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic

from . import models
from . import forms
from profiles.models import Notification


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
                position = form.save(commit=False)
                position.related_project = project
                position.save()
                project.positions.add(position)
            messages.add_message(
                self.request, messages.SUCCESS, "Project created successfully!"
            )
            return HttpResponseRedirect(
                reverse('projects:view-project', kwargs={'pk': project.pk})
            )
        messages.add_message(
            self.request,
            messages.ERROR,
            "Something went wrong! Please check fields with errors..."
        )
        return render(
            self.request,
            self.template_name,
            {
                'project_form': project_form,
                'position_formset': position_formset
            }
        )


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
                    position = form.save(commit=False)
                    position.related_project = project
                    position.save()
                    project.positions.add(position)
            messages.add_message(
                self.request, messages.SUCCESS, "Project updated successfully!"
            )
            return self.get_success_url()
        messages.add_message(
            self.request,
            messages.ERROR,
            "Something went wrong! Please check fields with errors..."
        )
        return self.render_to_response(
            self.get_context_data(
                object=self.object,
                project_form=project_form,
                position_formset=position_formset)
        )

    def get(self, request, *args, **kwargs):
        super(ProjectEditView, self).get(request, *args, **kwargs)
        project_form = self.form_class(instance=self.object)
        positions = self.object.positions.all()
        data = [{
            'title': position.title,
            'description': position.description,
            'related_skill': position.related_skill
        } for position in positions]
        if not data:
            position_formset = forms.PositionFormSet(
                initial=[{'title': '', 'description': ''}]
            )
        else:
            position_formset = forms.PositionFormSet(initial=data)
        return self.render_to_response(
            self.get_context_data(
                project_form=project_form,
                position_formset=position_formset
            )
        )


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
        context['active_projects'] = self.get_queryset().filter(
            completed=False
        )
        context['past_projects'] = self.get_queryset().filter(completed=True)
        context['positions'] = models.Position.objects.all()
        context['skills'] = [
            position.related_skill
            for position in models.Position.objects.filter(
                id__in=models.Position.objects.all().values_list(
                    'related_skill', flat=True).distinct()
            )
        ]
        return context


class ProjectFilterView(generic.ListView):
    model = models.Project
    template_name = "index.html"

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        query_set = models.Project.objects.filter(
            Q(positions__title=slug) | Q(positions__related_skill__skill=slug)
        )
        return query_set

    def get_context_data(self, **kwargs):
        context = super(ProjectFilterView, self).get_context_data(**kwargs)
        context['active_projects'] = self.get_queryset().filter(
            completed=False
        )
        context['past_projects'] = self.get_queryset().filter(completed=True)
        context['positions'] = models.Position.objects.all()
        context['skills'] = [
            position.related_skill
            for position in models.Position.objects.filter(
                id__in=models.Position.objects.all().values_list(
                    'related_skill', flat=True).distinct()
            )
        ]
        context['selected'] = self.kwargs.get('slug')
        return context


class ProjectChangeStatusView(generic.RedirectView):

    query_string = True
    pattern_name = 'projects:view-project'

    def get_redirect_url(self, *args, **kwargs):
        project = get_object_or_404(models.Project, pk=kwargs.get('pk'))
        if project.completed:
            project.completed = False
            for position in project.positions.all():
                if position.filled_by:
                    Notification.objects.get_or_create(
                        user=position.filled_by,
                        message="The project {} is now open.".format(project))
        else:
            project.completed = True
            for position in project.positions.all():
                if position.filled_by:
                    Notification.objects.get_or_create(
                        user=position.filled_by,
                        message="The project {} is now closed.".format(project)
                    )
        project.save()
        return super(
            ProjectChangeStatusView, self).get_redirect_url(*args, **kwargs)


class ApplicationView(generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        project = get_object_or_404(
            models.Project,
            pk=kwargs.get('project_pk')
        )
        position = get_object_or_404(models.Position, pk=kwargs.get('pk'))
        application, _ = models.Application.objects.get_or_create(
            applicant=self.request.user,
            position=position
        )
        Notification.objects.get_or_create(
            user=self.request.user,
            message="You've applied to {} position for {} project.".format(
                position, project
            )
        )
        position.applications.add(application)
        return reverse_lazy('projects:view-project', kwargs={'pk': project.pk})


class ApplicationListView(generic.ListView):
    template_name = 'projects/applications.html'

    def get_queryset(self):
        return models.Application.objects.filter(
            position__project__owner=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super(ApplicationListView, self).get_context_data(**kwargs)
        projects = models.Project.objects.filter(owner=self.request.user)
        positions = []
        for project in projects:
            for position in project.positions.all():
                positions.append(position)
        context['projects'] = projects
        context['positions'] = positions
        context['applications'] = self.get_queryset()
        context['status_filter'] = 'all'
        context['project_filter'] = 0
        context['position_filter'] = 0
        return context


class ApplicationFilterView(generic.ListView):
    template_name = 'projects/applications.html'

    def filter_status(self, query_set):
        status = self.kwargs.get('status')
        if status == 'new':
            return query_set.filter(accepted=False, rejected=False)
        elif status == 'accepted':
            return query_set.filter(accepted=True)
        elif status == 'rejected':
            return query_set.filter(rejected=True)
        return query_set

    def filter_projects(self, query_set):
        project_pk = self.kwargs.get('project_pk')
        if project_pk != '0':
            return query_set.filter(position__project__pk=project_pk)
        return query_set

    def filter_positions(self, query_set):
        position_pk = self.kwargs.get('position_pk')
        if position_pk != '0':
            return query_set.filter(position__pk=position_pk)
        return query_set

    def get_queryset(self):
        query_set = models.Application.objects.filter(
            position__project__owner=self.request.user
        )
        return self.filter_positions(
            self.filter_projects(self.filter_status(query_set))
        )

    def get_context_data(self, **kwargs):
        context = super(ApplicationFilterView, self).get_context_data(**kwargs)
        projects = models.Project.objects.filter(owner=self.request.user)
        positions = []
        for project in projects:
            for position in project.positions.all():
                positions.append(position)
        context['projects'] = projects
        context['positions'] = positions
        context['applications'] = self.get_queryset()
        context['status_filter'] = self.kwargs.get('status')
        context['project_filter'] = int(self.kwargs.get('project_pk'))
        context['position_filter'] = int(self.kwargs.get('position_pk'))
        return context


class ApplicationStatusView(generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        application = get_object_or_404(
            models.Application,
            pk=kwargs.get('pk')
        )
        position = application.position
        if kwargs.get('status') == 'accept':
            application.accepted = True
            application.save()
            Notification.objects.get_or_create(
                user=application.applicant,
                message="Your application on {} has been accepted.".format(
                    application.position)
            )
            position.filled = True
            position.filled_by = application.applicant
            position.save()
            for app in position.applications.all():
                if not app.accepted:
                    app.rejected = True
                    Notification.objects.get_or_create(
                        user=app.applicant,
                        message="Your application on "
                                "{} has been rejected.".format(app.position)
                    )
                    app.save()
        else:
            application.rejected = True
            application.save()
            Notification.objects.get_or_create(
                user=application.applicant,
                message="Your application on "
                        "{} has been rejected.".format(application.position))
        return self.request.META['HTTP_REFERER']
