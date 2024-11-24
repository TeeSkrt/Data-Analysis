from django.contrib import admin
from .models import Base

class BaseAdmin(admin.ModelAdmin):
    list_display = (
        'asin', 
        'product', 
        'category_name', 
        'image', 
        'rating', 
        'avg_rating', 
        'review', 
        'avg_review', 
        'price', 
        'avg_price', 
        'price_ratio', 
        'review_rating_ratio', 
        'relative_popularity', 
        'review_avg_review_ratio', 
        'amount', 
        'best_seller'
    )
    list_filter = ('category_name', 'best_seller')  # Lọc dữ liệu theo cột
    search_fields = ('asin', 'product', 'category_name')  # Tìm kiếm theo các cột này

# Register your models here.
admin.site.register(Base, BaseAdmin)