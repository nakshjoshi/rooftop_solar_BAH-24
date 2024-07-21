from django.db import models

# Create your models here.
class Feature(models.Model):
    name = models.CharField(max_length=250, help_text='Feature Name', default="House")
    description = models.TextField(help_text='Feature Description', default="Description")
    latitude = models.FloatField(help_text='Latitude')
    longitude = models.FloatField(help_text='Longitude')


    class Meta:
        verbose_name = ("feature")
        verbose_name_plural = ("features")

    def __str__(self):
        return f'{self.name}'
