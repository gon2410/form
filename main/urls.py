from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.render_index),
    path("validate", views.validate_input),
    path("creategroup", views.create_group),
    path("administracion", views.render_admin),
    path("get/<int:invited_id>", views.get_invite_data),
    path("update", views.update_invite),
    path("delete/<int:invite_id>", views.delete_invite),
    path("login", views.Login.as_view()),
    path("logout", views.logout_admin),
]