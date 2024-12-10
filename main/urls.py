from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.render_index),
    path("administracion", views.render_admin),
    path("addgroup", views.add_group),
    path("get/group/<int:group_id>", views.get_group),
    path("get/<int:guest_id>", views.get_guest),
    path("update", views.update_guest),
    path("delete/group/<int:group_id>", views.delete_group),
    path("delete/<int:guest_id>", views.delete_guest),
    path("validate", views.validate_input),
    path("download", views.download),
    path("login", views.Login.as_view()),
    path("logout", views.logout_admin),
]