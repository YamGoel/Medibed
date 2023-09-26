from django.db import models

# Create your models here.
class feedback(models.Model):
    full_name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    feed=models.TextField(max_length=500)

    def __str__(self):
        return self.full_name
