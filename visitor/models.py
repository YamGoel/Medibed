from django.db import models

# Create your models here.
class visitor(models.Model):
    id=models.BigAutoField(primary_key=True)
    username=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    city=models.CharField(max_length=100,null=True)
    password=models.CharField(max_length=20)

    def __str__(self):
        return self.username

class booked(models.Model):
    id=models.BigAutoField(primary_key=True)
    username=models.CharField(max_length=100)
    vis_email=models.EmailField(max_length=100,null=True)
    hospital_name = models.CharField(max_length=100)
    hospital_city = models.CharField(max_length=100)
    hospital_email = models.EmailField(max_length=100,null=True)

    def __str__(self):
        return self.username
