from django.db import models

class Example(models.Model):
    name = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)

class SubExample(models.Model):
    name = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)
    # https://docs.djangoproject.com/en/5.0/ref/models/fields/#foreignkey
    example = models.ForeignKey("Example", null=True, on_delete=models.SET_NULL)