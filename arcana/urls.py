from django.contrib import admin
from django.urls import path
from tarot import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("cards/", views.cards, name="cards"),
    path("cards/<slug:slug>/", views.card_detail, name="card_detail"),
    path("spreads/", views.spreads, name="spreads"),
    path("reading/", views.reading, name="reading"),
    path("about/", views.about, name="about"),
    path("astrology/", views.astrology, name="astrology"),
]
