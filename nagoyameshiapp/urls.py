from django.urls import path
from .import views

app_name    = "nagoyameshiapp"
urlpatterns = [
    path("", views.index, name="index"),

    path("restaurant/<int:pk>/", views.restaurant, name="restaurant" ),
                            #↑最後のスラッシュを入れておくこと

    path("review/<int:pk>/", views.review, name="review"),

    path("favorite/<int:pk>/", views.favorite, name="favorite"),

    path("reservation/<int:pk>/", views.reservation, name="reservation"),

]