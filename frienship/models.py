from django.db import models
from django.conf import settings
# Create your models here.


class Friendship(models.Model):
    
    choices = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=20, choices=choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ['sender', 'receiver'] #sender and receiver cannot be the same user
        ordering = ['-created_at']
        verbose_name = 'Friendship'
        verbose_name_plural = 'Friendships'
        
