from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^(?P<pk>\d+)$", views.ProfileView.as_view(), name="view-profile"),
    url(r"^edit/$", views.ProfileEditView.as_view(), name="edit-profile"),
    url(r"notifications/$", views.NotificationsView.as_view(), name="notifications"),
    url(r"notifications/read/(?P<pk>\d+)$", views.NotificationReadView.as_view(), name="notifications-read"),
    url(r"notifications/delete/(?P<pk>\d+)$", views.NotificationDeleteView.as_view(), name="notifications-delete"),
]
