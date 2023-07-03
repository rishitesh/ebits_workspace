from datetime import datetime

from django.db import models


class PostText(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=20)

    description = models.TextField()

    def __str__(self):
        return "%s->%s" % (self.id, self.type_name)


class CommonImage(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=40)
    image_url = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return "%s->%s" % (self.id, self.type_name)    
