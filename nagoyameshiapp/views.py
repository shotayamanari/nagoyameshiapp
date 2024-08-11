from django.shortcuts import render, redirect
from django.views import View

from .models import Category,Restaurant,Review,Favorite,Reservation,PremiumUser

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


        sort = "id"
        if "options" in request.GET:
            sort = request.GET["options"]

        context["restaurants"] = Restaurant.objects.filter(query).order_by(sort)
        context["newrestaurants"] = Restaurant.objects.order_by('-created_at')[:5]
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

        premium_user = PremiumUser.objects.filter(user=request.user).first()

        if not premium_user:
            print("カスタマーIDがセットされていません。")
            return redirect("nagoyameshiapp:index")


        # カスタマーIDを元にStripeに問い合わせ
        try:
            subscriptions = stripe.Subscription.list(customer=premium_user.premium_code)
        except:
            print("このカスタマーIDは無効です。")

            premium_user.delete()

            return redirect("nagoyameshiapp:index")

        is_active = False

        # ステータスがアクティブであるかチェック。
        for subscription in subscriptions.auto_paging_iter():
            if subscription.status == "active":
                print("サブスクリプションは有効です。")
                is_active = True
                
            else:
                print("サブスクリプションが無効です。")

        if not is_active:
                return redirect("nagoyameshiapp:mypage")

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

        ## 有料会員の確認 start ##
        premium_user = PremiumUser.objects.filter(user=request.user).first()

        if not premium_user:
            print("カスタマーIDがセットされていません。")
            return redirect("nagoyameshiapp:index")


        # カスタマーIDを元にStripeに問い合わせ
        try:
            subscriptions = stripe.Subscription.list(customer=premium_user.premium_code)
        except:
            print("このカスタマーIDは無効です。")

            premium_user.delete()

            return redirect("nagoyameshiapp:index")

        is_active = False

        # ステータスがアクティブであるかチェック。
        for subscription in subscriptions.auto_paging_iter():
            if subscription.status == "active":
                print("サブスクリプションは有効です。")
                is_active = True
                
            else:
                print("サブスクリプションが無効です。")

        if not is_active:
                return redirect("nagoyameshiapp:mypage")

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
        
        ## 有料会員の確認 end ##

        context = {}
        context["review"] = Review.objects.filter(id=pk,user=request.user).first()

        return render(request, "nagoyameshiapp/review_edit.html",context)


        #                   ↓このpkは編集したいレビューのidを示す
    def post(self, request, pk, *args, **kwargs):

        ## 有料会員の確認 start ##
        premium_user = PremiumUser.objects.filter(user=request.user).first()

        if not premium_user:
            print("カスタマーIDがセットされていません。")
            return redirect("nagoyameshiapp:index")


        # カスタマーIDを元にStripeに問い合わせ
        try:
            subscriptions = stripe.Subscription.list(customer=premium_user.premium_code)
        except:
            print("このカスタマーIDは無効です。")

            premium_user.delete()

            return redirect("nagoyameshiapp:index")

        is_active = False

        # ステータスがアクティブであるかチェック。
        for subscription in subscriptions.auto_paging_iter():
            if subscription.status == "active":
                print("サブスクリプションは有効です。")
                is_active = True
                
            else:
                print("サブスクリプションが無効です。")

        if not is_active:
                return redirect("nagoyameshiapp:mypage")

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
        
        ## 有料会員の確認 end ##

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
        ## 有料会員の確認 start ##
        premium_user = PremiumUser.objects.filter(user=request.user).first()

        if not premium_user:
            print("カスタマーIDがセットされていません。")
            return redirect("nagoyameshiapp:index")


        # カスタマーIDを元にStripeに問い合わせ
        try:
            subscriptions = stripe.Subscription.list(customer=premium_user.premium_code)
        except:
            print("このカスタマーIDは無効です。")

            premium_user.delete()

            return redirect("nagoyameshiapp:index")

        is_active = False

        # ステータスがアクティブであるかチェック。
        for subscription in subscriptions.auto_paging_iter():
            if subscription.status == "active":
                print("サブスクリプションは有効です。")
                is_active = True
                
            else:
                print("サブスクリプションが無効です。")

        if not is_active:
                return redirect("nagoyameshiapp:mypage")

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
        ## 有料会員の確認 end ##


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
        ## 有料会員の確認 start ##
        premium_user = PremiumUser.objects.filter(user=request.user).first()

        if not premium_user:
            print("カスタマーIDがセットされていません。")
            return redirect("nagoyameshiapp:index")


        # カスタマーIDを元にStripeに問い合わせ
        try:
            subscriptions = stripe.Subscription.list(customer=premium_user.premium_code)
        except:
            print("このカスタマーIDは無効です。")

            premium_user.delete()

            return redirect("nagoyameshiapp:index")

        is_active = False

        # ステータスがアクティブであるかチェック。
        for subscription in subscriptions.auto_paging_iter():
            if subscription.status == "active":
                print("サブスクリプションは有効です。")
                is_active = True
                
            else:
                print("サブスクリプションが無効です。")

        if not is_active:
                return redirect("nagoyameshiapp:mypage")

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
        
        ## 有料会員の確認 end ##

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
        ## 有料会員の確認 start ##
        premium_user = PremiumUser.objects.filter(user=request.user).first()

        if not premium_user:
            print("カスタマーIDがセットされていません。")
            return redirect("nagoyameshiapp:index")

        # カスタマーIDを元にStripeに問い合わせ
        try:
            subscriptions = stripe.Subscription.list(customer=premium_user.premium_code)
        except:
            print("このカスタマーIDは無効です。")

            premium_user.delete()

            return redirect("nagoyameshiapp:index")

        is_active = False

        # ステータスがアクティブであるかチェック。
        for subscription in subscriptions.auto_paging_iter():
            if subscription.status == "active":
                print("サブスクリプションは有効です。")
                is_active = True
                
            else:
                print("サブスクリプションが無効です。")

        if not is_active:
                return redirect("nagoyameshiapp:mypage")

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
        ## 有料会員の確認 end ##        

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

        # PremiumUserのデータがあるか否かを確認する
        context["is_premium"] = PremiumUser.objects.filter(user=request.user).exists()


        return render(request, "nagoyameshiapp/mypage.html",context)
    
    def post(self, request, *args, **kwargs):
        pass

mypage = MypageView.as_view()




# =========== stripe サブスクリプション関係のビュー ==============
from django.conf import settings
from django.urls import reverse_lazy

import stripe
stripe.api_key  = settings.STRIPE_API_KEY

# セッションを作っている
class CheckoutView(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):

        # ↓3: Stripeがセッションを作る        # ↓ 2:セッションを作ってくれ。
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': settings.STRIPE_PRICE_ID,
                    'quantity': 1,
                },
            ],
            payment_method_types=['card'],
            mode='subscription',

            # カード決済完了時のリダイレクト先の設定。(外部サイト(stripe)へ行く仕様上、URLは絶対パスでないといけない)
            success_url=request.build_absolute_uri(reverse_lazy("nagoyameshiapp:success")) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse_lazy("nagoyameshiapp:index")),
        )

        # セッションid
        print( checkout_session["id"] )

        # 4: 決済ページへクライアントをリダイレクトさせる。
        return redirect(checkout_session.url)

checkout    = CheckoutView.as_view()


# 5: stripeのサイトでカード情報を入力する。
# カード情報は 4242424242424242424242....
# それ以外は適当でOK success_urlヘリダイレクトされる。

# 8: 決済情報のチェック。パラメータのセッションidを使ってチェックをする。
class SuccessView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):

        # パラメータにセッションIDがあるかチェック
        if "session_id" not in request.GET:
            print("セッションIDがありません。")
            return redirect("nagoyameshiapp:index")

        # ?session_id=adaijdoajdiaojdoaijdoj
        # そのセッションIDは有効であるかチェック。
        try:
            checkout_session_id = request.GET['session_id']
            checkout_session    = stripe.checkout.Session.retrieve(checkout_session_id)
        except:
            print( "このセッションIDは無効です。")
            return redirect("nagoyameshiapp:index")

        print(checkout_session)

        # statusをチェックする。未払であれば拒否する。(未払いのsession_idを入れられたときの対策)
        if checkout_session["payment_status"] != "paid":
            print("未払い")
            return redirect("nagoyameshiapp:index")

        print("支払い済み")

        """
        # 有効であれば、セッションIDからカスタマーIDを取得。ユーザーモデルへカスタマーIDを記録する。
        request.user.customer   = checkout_session["customer"]
        request.user.save()
        """

        # PremiumUserを使って、カスタマーidを記録する。
        premium_user = PremiumUser()
        premium_user.user = request.user
        premium_user.premium_code = checkout_session["customer"]

        premium_user.save()



        print("有料会員登録しました！")

        # 実践ではありがとうございましたのページを表示する。
        return redirect("nagoyameshiapp:index")

success     = SuccessView.as_view()


# サブスクリプションの操作関係
class PortalView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        premium_user = PremiumUser.objects.filter(user=request.user).first()

        if not premium_user:
            print( "有料会員登録されていません")
            return redirect("nagoyameshiapp:index")

        # ユーザーモデルに記録しているカスタマーIDを使って、ポータルサイトへリダイレクト
        portalSession   = stripe.billing_portal.Session.create(
            customer    = premium_user.premium_code,
            return_url  = request.build_absolute_uri(reverse_lazy("nagoyameshiapp:index")),
        )

        return redirect(portalSession.url)

portal      = PortalView.as_view()


class PremiumView(View):
    def get(self, request, *args, **kwargs):
        

        # TODO: ↓ お気に入り・レビュー・予約のビューに入れる。
        premium_user = PremiumUser.objects.filter(user=request.user).first()

        if not premium_user:
            print("カスタマーIDがセットされていません。")
            return redirect("nagoyameshiapp:index")


        # カスタマーIDを元にStripeに問い合わせ
        try:
            subscriptions = stripe.Subscription.list(customer=premium_user.premium_code)
        except:
            print("このカスタマーIDは無効です。")

            premium_user.delete()

            return redirect("nagoyameshiapp:index")

        is_active = False

        # ステータスがアクティブであるかチェック。
        for subscription in subscriptions.auto_paging_iter():
            if subscription.status == "active":
                print("サブスクリプションは有効です。")
                is_active = True
                
            else:
                print("サブスクリプションが無効です。")

        if is_active:
                return render(request, "nagoyameshiapp/premium.html")

        return redirect("nagoyameshiapp:index")

premium     = PremiumView.as_view()



