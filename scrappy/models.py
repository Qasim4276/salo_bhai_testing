from django.db import models

class Playlist(models.Model):
    file = models.FileField(upload_to='media/playlists/',null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True,null=True)
    file_name = models.CharField(max_length=255,null=True)
class Channel(models.Model):
    file = models.FileField(upload_to='media/channels/',null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True,null=True)
    file_name = models.CharField(max_length=255,null=True)