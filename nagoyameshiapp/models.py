from typing import Any
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    name        = models.CharField(verbose_name="名前", max_length=15)
    created_at  = models.DateTimeField(verbose_name="作成日時", default=timezone.now)
    updated_at  = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    category    = models.ForeignKey(Category, verbose_name="カテゴリ", on_delete=models.CASCADE)

    name        = models.CharField(verbose_name="名前", max_length=50)
    image       = models.ImageField(verbose_name="画像", upload_to="nagoyameshiapp/restaurant/image/",blank=True,null=True)
    description = models.CharField(verbose_name="店舗説明", max_length=500)
    start_at    = models.TimeField(verbose_name="営業開始時間", default=timezone.now)
    end_at      = models.TimeField(verbose_name="営業終了時間", default=timezone.now)
    cost        = models.PositiveIntegerField(verbose_name="価格帯", blank=True, null=True)
    post_code   = models.CharField(verbose_name="郵便番号", max_length=8, blank=True, null=True)
    address     = models.CharField(verbose_name="住所", max_length=100, blank=True)
    tel         = models.CharField(verbose_name="電話番号", max_length=11, blank=True, null=True)
    created_at  = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)
    updated_at  = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    restaurant  = models.ForeignKey(Restaurant, verbose_name="店舗", on_delete=models.CASCADE)
    user        = models.ForeignKey(User, verbose_name="投稿者", on_delete=models.CASCADE)

    content     = models.CharField(verbose_name="内容", max_length=100)
    created_at  = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)
    updated_at  = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):
        return self.user


class Favorite(models.Model):
    uesr        = models.ForeignKey(User, verbose_name="予約者", on_delete=models.CASCADE)
    restaurant  = models.ForeignKey(Restaurant, verbose_name="店舗", on_delete=models.CASCADE)

    created_at  = models.DateTimeField(verbose_name="作成日時", default=timezone.now)

    def __str__(self):
        return self.user


class Reservation(models.Model):
    user        = models.ForeignKey(User, verbose_name="予約者", on_delete=models.CASCADE)
    restaurant  = models.ForeignKey(Restaurant, verbose_name="店舗", on_delete=models.CASCADE)

    datetime    = models.DateTimeField(verbose_name="予約日時")
    headcount   = models.PositiveIntegerField(verbose_name="人数")

    created_at  = models.DateTimeField(verbose_name="作成日時", default=timezone.now)
    updated_at  = models.DateTimeField(verbose_name="更新日時", auto_now=True)


class PremiumUser(models.Model):
    user        = models.ForeignKey(User, verbose_name="会員", on_delete=models.CASCADE)

    premium_code= models.TextField(verbose_name="有料会員コード")
