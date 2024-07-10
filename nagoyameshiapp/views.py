from django.shortcuts import render, redirect
from django.views import View

from .models import Category,Restaurant,Review,Favorite,Reservation

from .forms import RestaurantCategoryForm,ReviewForm,FavoriteForm,ReservationForm

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

        if Favorite.objects.filter(restaurant=pk, user=request.user):
            context["is_favorite"] = True
        else:
            context["is_favorite"] = False

        return render(request, "nagoyameshiapp/restaurant.html", context)
# urls.pyから呼び出ししやすいようにする
restaurant = RestaurantView.as_view()



# レビュー投稿用のビュー
class ReviewView(View):
    def post(self, request, pk, *args, **kwargs):

        # request.POSTの内容を書き換え可能にする。
        copied = request.POST.copy()
        copied["restaurant"]    = pk
        copied["user"]          = request.user

        # copiedをバリデーションする。
        form = ReviewForm(copied)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        return redirect("nagoyameshiapp:restaurant", pk)
# urls.pyから呼び出ししやすいようにする
review = ReviewView.as_view()


# お気に入り登録用のビュー
class FavoriteView(View):
    def post(self, request, pk, *args, **kwargs):

        # 店舗のお気に入り登録 
        print("お気に入り登録をする")

        # すでにお気に入り登録されているかチェックする
        favorites   = Favorite.objects.filter(restaurant=pk, user=request.user)
        if favorites:
            favorites.delete()
            # すでにお気に入りのデータがある場合は削除する
        else: 
            #データがない場合は登録する
            dic     = {}
            dic["restaurant"]   = pk
            dic["user"]         = request.user

            form    = FavoriteForm(dic)

            if form.is_valid():
                print("お気に入り登録")
                form.save()
            else:
                print(form.errors)

        return redirect("nagoyameshiapp:restaurant", pk)
# urls.pyから呼び出ししやすいようにする
favorite = FavoriteView.as_view()


class ReservationView(View):
    def post(self, request, pk, *args, **kwargs):
        
        print("予約します")

        copied = request.POST.copy()
        copied["restaurant"]    = pk
        copied["user"]          = request.user

        form = ReservationForm(copied)

        if form.is_valid():
            print("予約")
            form.save()
        else:
            print(form.errors)

        return redirect("nagoyameshiapp:restaurant", pk)

reservation = ReservationView.as_view()