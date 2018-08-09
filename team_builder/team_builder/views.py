from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = "index.html"
