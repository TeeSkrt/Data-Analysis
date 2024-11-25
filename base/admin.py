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
        'price_amount_ratio',
        'rating_review_ratio',
        'popularity_global_ratio',
        'popularity_category_max_ratio',
        'price_rating_interaction',
        'review_amount_interaction',
        'combined_interaction',
        'amount', 
        'predicted_best_seller'
    )
    list_filter = ('category_name', 'predicted_best_seller', 'amount', 'rating', 'price', 'review')  
    search_fields = ('asin', 'product', 'category_name', 'predicted_best_seller')  

# Register your models here.
admin.site.register(Base, BaseAdmin)
