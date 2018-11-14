from django.conf import settings
from django.db import models


# Create your models here.

class Images(models.Model):
    class Meta:
        db_table = "images"

    title = models.CharField(max_length=512, null=False)
    images_tag = models.CharField(max_length=512)
    users = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=False,
                              on_delete=models.CASCADE,
                              default=1)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    description = models.TextField(null=True, blank=True, default="")
    image = models.ImageField(null=True, width_field="width_field",
                              height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
