from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from .validator import validate_is_torrent

# Create your models here.

CAT_LIST= (

    ("Documents", "Documents"),
    ("Videos", "Video"),
    ("Research", "Research"),
    ("Software" ,"Software"),
    ("Other", "Other"),
  
)

class TorFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=200)
    desc = models.TextField(max_length=1000)
    file_field = models.FileField(upload_to="uploads/",validators=[validate_is_torrent,])
    date = models.DateField(auto_now_add=True)
    file_size = models.CharField(max_length=20, default=0)
    magnet = models.CharField(max_length=200, default="")
    infohash = models.CharField(max_length=200, default=0)
    total_completed = models.IntegerField(default=0)
    total_seeds = models.IntegerField(default=0)
    total_leechers = models.IntegerField(default=0)
    category = models.CharField(max_length=10, choices=CAT_LIST,default="None")

    def __str__(self):
        return self.title
    