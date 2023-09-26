from django.db import models

# Create your models here.
class hospital(models.Model):
    id=models.BigAutoField(primary_key=True)
    hospital_username=models.CharField(max_length=100)
    hospital_name=models.CharField(max_length=100)
    hospital_city=models.CharField(max_length=100,null=True)
    hospital_email=models.EmailField(max_length=100)
    address=models.TextField(max_length=100)
    password=models.CharField(max_length=20)

    def __str__(self):
        return self.hospital_name


class bedsubmit(models.Model):
    id=models.BigAutoField(primary_key=True)
    hospital_name=models.CharField(max_length=100)
    hospital_city=models.CharField(max_length=100)
    beds=models.CharField(max_length=10000,null=True)
    occupied=models.CharField(max_length=10000,null=True)
    available=models.CharField(max_length=10000,null=True)
    price=models.IntegerField(null=True)

    def __str__(self):
        return self.hospital_name
