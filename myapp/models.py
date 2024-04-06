from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True)  # store current timestamp
    created = models.DateTimeField(
        auto_now_add=True
    )  # initial timestamp doesn't change

    class Meta:
        # displaying recently created room at the top
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE
    )  # if the parent is deleted, delete all the child
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)  # store current timestamp
    created = models.DateTimeField(
        auto_now_add=True
    )  # initial timestamp doesn't change

    def __str__(self):
        return self.body[0:50]  # display first 50 character
