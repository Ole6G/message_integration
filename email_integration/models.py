from django.db import models


class UserEmail(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=100)


class Message(models.Model):
    subject = models.CharField(max_length=255)
    send_date = models.DateTimeField()
    received_date = models.DateTimeField()
    description = models.TextField()
    attachments = models.JSONField()

