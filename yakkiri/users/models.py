from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    STATUS_CHOICES = (
            ('doctor', '의사'),
            ('pharmacist', '약사'),
            ('general', '일반인'),
            ('other', '기타')
        )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='general')