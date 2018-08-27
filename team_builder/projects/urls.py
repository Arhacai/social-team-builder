from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^(?P<pk>\d+)$", views.ProjectView.as_view(), name="view-project"),
    url(r"^new/$", views.ProjectCreateView.as_view(), name="create-project"),
    url(
        r"^edit/(?P<pk>\d+)$",
        views.ProjectEditView.as_view(),
        name="edit-project"),
    url(
        r"^delete/(?P<pk>\d+)",
        views.ProjectDeleteView.as_view(),
        name="delete-project"),
    url(r'^search/', views.ProjectSearchView.as_view(), name="search"),
    url(
        r"^filter/(?P<slug>[-_\s\w\d]+)",
        views.ProjectFilterView.as_view(),
        name="filter"),
    url(
        r"^status/(?P<pk>\d)$",
        views.ProjectChangeStatusView.as_view(),
        name="change-status"),
    url(
        r"^applications/$",
        views.ApplicationListView.as_view(),
        name="applications"),
    url(
        r"^applications/filter/(?P<status>\w+)/"
        r"(?P<project_pk>\d+)/(?P<position_pk>\d+)$",
        views.ApplicationFilterView.as_view(),
        name="status-filter"),
    url(
        r"^applications/(?P<pk>\d+)/(?P<status>\w+)$",
        views.ApplicationStatusView.as_view(),
        name="application-status"),
    url(
        r"^(?P<project_pk>\d+)/apply/(?P<pk>\d+)$",
        views.ApplicationView.as_view(),
        name="apply"),
]
