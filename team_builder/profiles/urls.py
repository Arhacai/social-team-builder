from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.ProfileView.as_view(), name="view-profile"),
    url(r"^edit/", views.ProfileEditView.as_view(), name="edit-profile"),
]
