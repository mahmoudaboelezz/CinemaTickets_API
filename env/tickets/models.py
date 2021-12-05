from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# Create your models here.

class Movie(models.Model):
    hall = models.CharField(verbose_name="hall", max_length=50)
    movie = models.CharField(verbose_name="movie", max_length=50)

    #date = models.DateField(auto_now=False, auto_now_add=False)
    
    def __str__(self):
        return self.movie

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
    
class Guest(models.Model):
    name = models.CharField( max_length=10)
    mobile = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name
    
class Reservation(models.Model):
    guest = models.ForeignKey(Guest, related_name='reservation', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,related_name='reservation', on_delete=models.CASCADE)
    
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender,instance,created,**kwargs):
    if created:
        Token.objects.create(user=instance)