from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Kategori(models.Model):
    isim = models.CharField(max_length=100)
    def __str__(self):
        return self.isim
    
class Product(models.Model):
    kategori = models.ForeignKey(Kategori, on_delete = models.SET_NULL, null=True, blank=True)
    isim = models.CharField(max_length=100)
    fiyat = models.IntegerField()
    resim = models.FileField(upload_to = 'product/', null=True)

    def __str__(self):
        return self.isim

class Basket(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number = models.IntegerField()
    totalPrice = models.IntegerField()
    payment = models.BooleanField(default=False)

    def __str__(self):
        return self.product.isim

class Payment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    basket = models.ManyToManyField(Basket, related_name='payments')
    totalPrice = models.IntegerField()
    payment = models.BooleanField(default=False)

    def __str__(self):
        return self.owner.username
