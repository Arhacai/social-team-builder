from django.views import generic

from projects import models


class Home(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data()
        context['active_projects'] = models.Project.objects.filter(completed=False)
        context['past_projects'] = models.Project.objects.filter(completed=True)
        context['positions'] = models.Position.objects.all()
        return context
