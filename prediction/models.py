from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class PredictionHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='predictions')
    image = models.ImageField(upload_to='predictions/')
    prediction_result = models.CharField(max_length=100)
    risk_percentage = models.FloatField()
    is_high_risk = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.prediction_result} - {self.created_at}"
