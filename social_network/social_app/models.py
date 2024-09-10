from django.contrib.auth.models import User
from django.db import models

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),  # Add this line if not already present
    ], default='pending')  # Default status is set to 'pending'

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.status})"
