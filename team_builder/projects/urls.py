from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^(?P<pk>\d+)$", views.ProjectView.as_view(), name="view-project"),
    url(r"^new/$", views.ProjectCreateView.as_view(), name="create-project"),
    url(r"^edit/(?P<pk>\d+)$", views.ProjectEditView.as_view(), name="edit-project"),
    url(r"^delete/(?P<pk>\d+)", views.ProjectDeleteView.as_view(), name="delete-project"),
    url(r'^search/', views.ProjectSearchView.as_view(), name="search"),
    url(r"^filter/(?P<title>[-*_*\s*\w+]+)", views.ProjectFilterView.as_view(), name="filter"),
    url(r"^status/(?P<pk>\d)$", views.ProjectChangeStatusView.as_view(), name="change-status"),
]
