from django.urls import path
from backend import views

urlpatterns = [
    path("visit", views.visit, name="visit"),
    path("visit_result/<slug:ref>", views.visit_result, name="visit_result"),
]
