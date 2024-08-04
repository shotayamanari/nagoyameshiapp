from django.urls import path
from .import views

app_name    = "nagoyameshiapp"
urlpatterns = [
    path("", views.index, name="index"),

    path("restaurant/<int:pk>/", views.restaurant, name="restaurant" ),
                            #↑最後のスラッシュを入れておくこと
    path("review/<int:pk>/", views.review, name="review"),
    
    path("review_edit/<int:pk>/", views.review_edit, name="review_edit"),

    path("review_delete/<int:pk>/", views.review_delete, name="review_delete"),

    path("favorite/<int:pk>/", views.favorite, name="favorite"),

    path("reservation/<int:pk>/", views.reservation, name="reservation"),

    path("reservation_delete/<int:pk>/", views.reservation_delete, name="reservation_delete"),

    path("mypage/", views.mypage, name="mypage"),


    path("checkout/", views.checkout, name="checkout"),
    path("success/", views.success, name="success"),
    path("portal/", views.portal, name="portal"),
    path("premium/", views.premium, name="premium"),

]