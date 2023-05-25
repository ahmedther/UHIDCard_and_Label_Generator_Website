from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("mumbai", views.mumbai, name="mumbai"),
    path("indore", views.indore, name="indore"),
    path("ip_label", views.ip_label, name="ip_label"),
    path("op_label", views.op_label, name="op_label"),
    path("both_label", views.both_label, name="both_label"),
    path("lebel_with_spec", views.lebel_with_spec, name="lebel_with_spec"),
]
