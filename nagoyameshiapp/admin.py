from django.contrib import admin
from django.utils.html import format_html
from .models import Category,Restaurant,Review,Favorite,Reservation,PremiumUser

class RestaurantAdmin(admin.ModelAdmin):
    list_display    = ["category","name","description","format_photo"]

    search_fields   = ["name"]
    list_filter     = ["name"]

    list_per_page       = 10
    list_max_show_all   = 20000

    def format_photo(self,obj):
        if obj.image:
            return format_html('<img src="{}" alt="画像" style="width:15rem">', obj.image.url)
    
    format_photo.short_description      = Restaurant.image.field.verbose_name
    format_photo.empty_value_display    = "画像なし"

admin.site.register(Category)
admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(Review)
admin.site.register(Favorite)
admin.site.register(Reservation)
admin.site.register(PremiumUser)