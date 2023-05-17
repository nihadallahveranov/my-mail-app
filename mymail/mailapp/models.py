from django.db import models

class Mail(models.Model):
    sender = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)