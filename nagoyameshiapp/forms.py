from django import forms
from .models import Category,Restaurant,Review,Favorite,Reservation

class RestaurantCategoryForm(forms.ModelForm):
    class Meta:
        model  = Restaurant
        fields = [ "category" ]

class ReviewForm(forms.ModelForm):
    class Meta:
        model  = Review
        fields = [ "restaurant", "user", "content" ] 


# Favoriteのバリデーション用のフォーム
class FavoriteForm(forms.ModelForm):
    class Meta:
        model  = Favorite
        fields = [ "restaurant", "user" ]

class ReservationForm(forms.ModelForm):
    class Meta:
        model  = Reservation
        fields = [ "restaurant", "user", "datetime", "headcount" ]