from django.shortcuts import render, redirect
from django.views import View

from .models import Category,Restaurant,Review

from .forms import RestaurantCategoryForm,ReviewForm

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
        context["categories"]  = Category.objects.all()

        return render(request, "nagoyameshiapp/index.html", context)

# urls.pyから呼び出ししやすいようにする
index = IndexView.as_view()



# 個別ページを表示するビュー
class RestaurantView(View):

    def get(self, request, pk, *args, **kwargs):
        context = {}

        context["restaurant"] = Restaurant.objects.filter(id=pk).first()

        context["reviews"]    = Review.objects.filter(restaurant=pk)



        return render(request, "nagoyameshiapp/restaurant.html", context)

restaurant = RestaurantView.as_view()



# レビュー投稿用のビュー
class ReviewView(View):
    def post(self, request, pk, *args, **kwargs):

        form = ReviewForm(request.POST)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        return redirect("nagoyameshiapp:restaurant", pk)

review = ReviewView.as_view()