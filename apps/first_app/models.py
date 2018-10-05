from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Artwork(models.Model):
    user = models.ForeignKey(User, related_name = "users_artwork", on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    description = models.TextField()
    price = models.IntegerField()
    art_photo = models.ImageField(upload_to='art_photos/')
    art_file = models.FileField(upload_to='art_files/')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Cart(models.Model):
    user = models.ForeignKey(User, related_name = "users_cart", on_delete = models.CASCADE)
    artwork = models.ManyToManyField(Artwork, related_name= "carts")
