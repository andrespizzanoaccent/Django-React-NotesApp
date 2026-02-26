from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    metadata = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    body = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.body[0:50]
