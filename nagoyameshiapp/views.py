from django.shortcuts import render, redirect
from django.views import View

from .models import Category,Restaurant,Review,Favorite,Reservation

from .forms import RestaurantCategoryForm,ReviewForm,FavoriteForm,ReservationForm

from django.db.models import Q

from django.utils import timezone

import datetime

from django.contrib.auth.mixins import LoginRequiredMixin


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
class RestaurantView(LoginRequiredMixin,View):
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
class ReviewView(LoginRequiredMixin,View):
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


# レビュー編集用のビュー
class ReviewEditView(LoginRequiredMixin,View):
    def get(self, request, pk, *args, **kwargs):

        context = {}
        context["review"] = Review.objects.filter(id=pk,user=request.user).first()

        return render(request, "nagoyameshiapp/review_edit.html",context)

        #                   ↓このpkは編集したいレビューのidを示す
    def post(self, request, pk, *args, **kwargs):
       
        print("編集")

        # 編集したいレビューのオブジェクトを取り出す
        review = Review.objects.filter(id=pk,user=request.user).first()

        # request.POSTの内容を書き換え可能にする。
        copied = request.POST.copy()
        copied["restaurant"]    = review.restaurant
        copied["user"]          = request.user

        # 編集したい場合は、引数にreviewを入れる
        form = ReviewForm(copied,instance=review)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        # 編集を終えた後、店舗の個別ページに返す　　　　　↓
        return redirect("nagoyameshiapp:restaurant", review.restaurant.id)

review_edit = ReviewEditView.as_view()


# レビュー削除用のビュー
class ReviewDeleteView(LoginRequiredMixin,View):
    def post(self, request, pk, *args, **kwargs):

        review = Review.objects.filter(id=pk,user=request.user).first()

        # deleteメソッドを利用する
        review.delete()

        return redirect("nagoyameshiapp:restaurant", review.restaurant.id)

review_delete = ReviewDeleteView.as_view()

# 予約キャンセル用のビューを作成する
class ReservationDeleteView(LoginRequiredMixin,View):
    def post(self, request, pk, *args, **kwargs):

        reservation = Reservation.objects.filter(id=pk,user=request.user).first()

        # キャンセルできるのは、現在の日時から1日先の未来の予約だけにする
        deadline = timezone.now() + datetime.timedelta(days=1)

        if deadline < reservation.datetime:
            print("予約キャンセル")
            reservation.delete()

        return redirect("nagoyameshiapp:mypage")

reservation_delete = ReservationDeleteView.as_view()
        





# お気に入り登録用のビュー
class FavoriteView(LoginRequiredMixin,View):
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


# 予約登録用のビュー
class ReservationView(LoginRequiredMixin,View):
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


# マイページ用のビュー
class MypageView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        
        context = {}

        # 自分のレビューと予約とお気に入りを表示させる
        context["reviews"]     =  Review.objects.filter(user=request.user)
        context["favorites"]   =  Favorite.objects.filter(user=request.user)
        context["reservations"] =  Reservation.objects.filter(user=request.user)       

        # 予約の〆日をコンテキストに追加し、mypageのテンプレートで利用
        # 一日以上の予約
        context["deadline"]   =  timezone.now() + datetime.timedelta(days=1)

        return render(request, "nagoyameshiapp/mypage.html",context)
    
    def post(self, request, *args, **kwargs):
        pass

mypage = MypageView.as_view()



