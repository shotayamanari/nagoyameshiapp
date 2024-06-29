from django import forms
from .models import Category,Restaurant

class RestaurantCategoryForm(forms.ModelForm):
    class Meta:
        model  = Restaurant
        fields = ["category","name"]