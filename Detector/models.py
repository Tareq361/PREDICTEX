from django.db import models

# Create your models here.
class covidImages(models.Model):
    image = models.ImageField(blank=True, upload_to="covidimages")
