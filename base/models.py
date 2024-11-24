from django.db import models

# Create your models here.
class Base(models.Model):
    asin = models.CharField(max_length=255, unique=True, default="default_asin")  
    product = models.TextField(default="No Product Description")  
    category_name = models.CharField(max_length=255, default="Unknown")  
    image = models.URLField(default="")  
    rating = models.FloatField(default=0.0)  
    avg_rating = models.FloatField(default=0.0)  
    review = models.IntegerField(default=0)  
    avg_review = models.FloatField(default=0.0)  
    price = models.FloatField(default=0.0)  
    avg_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    price_ratio = models.FloatField(default=0.0)  
    review_rating_ratio = models.FloatField(default=0.0)  
    relative_popularity = models.FloatField(default=0.0)  
    review_avg_review_ratio = models.FloatField(default=0.0)  
    amount = models.IntegerField(default=0)  
    best_seller = models.BooleanField(default=False) 

    def _str_(self):
        return self.product