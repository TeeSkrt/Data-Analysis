from django.db import models

class Base(models.Model):
    asin = models.CharField(max_length=255, unique=True, default="default_asin", db_column="Asin")
    product = models.TextField(default="No Product Description", db_column="Product")
    category_name = models.CharField(max_length=255, default="Unknown", db_column="Category_name")
    image = models.URLField(default="", db_column="Image")
    rating = models.FloatField(default=0.0, db_column="Rating")
    avg_rating = models.FloatField(default=0.0, db_column="Avg_rating")
    review = models.IntegerField(default=0, db_column="Review")
    avg_review = models.FloatField(default=0.0, db_column="Avg_review")
    price = models.FloatField(default=0.0, db_column="Price")
    avg_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, db_column="Avg_price")
    price_ratio = models.FloatField(default=0.0, db_column="Price_Ratio")
    review_rating_ratio = models.FloatField(default=0.0, db_column="Review_Rating_Ratio")
    relative_popularity = models.FloatField(default=0.0, db_column="Relative_Popularity")
    review_avg_review_ratio = models.FloatField(default=0.0, db_column="Review_Avg_Review_Ratio")
    price_amount_ratio = models.FloatField(default=0.0, db_column="Price_Amount_Ratio")
    rating_review_ratio = models.FloatField(default=0.0, db_column="Rating_Review_Ratio")
    popularity_global_ratio = models.FloatField(default=0.0, db_column="Popularity_Global_Ratio")
    popularity_category_max_ratio = models.FloatField(default=0.0, db_column="Popularity_Category_Max_Ratio")
    price_rating_interaction = models.FloatField(default=0.0, db_column="Price_Rating_Interaction")
    review_amount_interaction = models.FloatField(default=0.0, db_column="Review_Amount_Interaction")
    combined_interaction = models.FloatField(default=0.0, db_column="Combined_Interaction")
    amount = models.IntegerField(default=0, db_column="Amount")
    predicted_best_seller = models.BooleanField(default=False, db_column="Predicted_Best_Seller")

    class Meta:
        managed = False
        db_table = "Predictions"  # Tên bảng trong SQL Server
        verbose_name = "Prediction"
        verbose_name_plural = "Predictions"

    def __str__(self):
        return self.asin