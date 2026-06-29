from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        BUYER = "BUYER", "Buyer"
        SELLER = "SELLER", "Seller"
        
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.BUYER
    )
    
    image = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone = models.CharField(max_length=13, help_text="+998919990033")
    address = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f'{self.username} -> {self.role}'    