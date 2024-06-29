from django.shortcuts import render
from django.views import View

from .models import Category,Restaurant

from .forms import RestaurantCategoryForm

from django.db.models import Q

class IndexView(View):
    def get(self, request, *args, **kwargs):
    
        context = {}

        query   = Q()

        form    = RestaurantCategoryForm(request.GET)

        if form.is_valid():
            cleaned = form.clean()

            query &= Q(category=cleaned["category"])

        if "search" in request.GET:
            words   = request.GET["search"].replace("　"," ").split(" ")

            for word in words:

                if word == "":
                    continue

                query &= Q(name__contains=word)

        context["restaurants"] = Restaurant.objects.filter(query)
        context["categories"]  = Category.objects.filter(query)

        return render(request, "nagoyameshiapp/index.html", context)

# urls.pyから呼び出ししやすいようにする
index = IndexView.as_view()