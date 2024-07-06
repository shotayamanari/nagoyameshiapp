from django import forms
from .models import Category,Restaurant,Review

class RestaurantCategoryForm(forms.ModelForm):
    class Meta:
        model  = Restaurant
        fields = ["category"]

class ReviewForm(forms.ModelForm):
    class Meta:
        model  = Review
        fields = ["restaurant","user","content"]