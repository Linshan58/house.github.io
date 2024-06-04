from django.db import models

# Create your models here.
#設定模型
"""
class RealEstateTransaction(models.Model):   

    class Meta:
        db_table = 'xx'  # 將此處替換為您的 MongoDB collection 名稱

    鄉鎮市區 = models.CharField(max_length=50)
    交易標的 = models.CharField(max_length=50)
    土地位置建物門牌 = models.CharField(max_length=255)
    土地移轉總面積平方公尺 = models.FloatField()
    都市土地使用分區 = models.CharField(max_length=50)
    交易年月日 = models.IntegerField()
    交易筆棟數 = models.CharField(max_length=50)
    移轉層次 = models.CharField(max_length=20)
    總樓層數 = models.CharField(max_length=20)
    建物型態 = models.CharField(max_length=50)
    主要用途 = models.CharField(max_length=50)
    主要建材 = models.CharField(max_length=50)
    建築完成年月 = models.IntegerField()
    建物移轉總面積平方公尺 = models.FloatField()
    建物現況格局_房 = models.IntegerField()
    建物現況格局_廳 = models.IntegerField()
    建物現況格局_衛 = models.IntegerField()
    建物現況格局_隔間 = models.CharField(max_length=10)
    有無管理組織 = models.CharField(max_length=10)
    總價元 = models.IntegerField()
    單價元平方公尺 = models.IntegerField()
    車位移轉總面積平方公尺 = models.FloatField()
    車位總價元 = models.IntegerField()
    備註 = models.TextField()
    編號 = models.CharField(max_length=20)
    主建物面積 = models.FloatField()
    附屬建物面積 = models.FloatField()
    陽台面積 = models.FloatField()
    電梯 = models.CharField(max_length=10)
    移轉編號 = models.IntegerField()
    房地_土地_建物 = models.IntegerField()
    車位有無 = models.IntegerField()
    土地 = models.IntegerField()
    建物 = models.IntegerField()
    車位 = models.IntegerField()
"""

#設計抓取商品資料
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')


#設計會員

class Member(models.Model):
    member_id = models.IntegerField(primary_key=True)
    account = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    favorites = models.ManyToManyField(Product)
    member_type = models.CharField(max_length=100, default="normal")

