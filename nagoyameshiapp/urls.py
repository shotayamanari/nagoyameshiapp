from django.urls import path
from .import views

app_name    = "nagoyameshiapp"
urlpatterns = [
    path("", views.index, name="index"),

    path("restaurant/<int:pk>/", views.restaurant, name="restaurant" ),

    path("review/<int:pk>", views.review, name="review"),

]