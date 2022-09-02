from django.db import models
from django.db.models.fields import Empty
# Create your models here.





class Audio_upload(models.Model):

  Upload_Audio = models.FileField()
  
  def __str__(self):
    return str(self.id)


class Ai_bot(models.Model):
  text = models.CharField(max_length=1000)
  Bot_Sound = models.FileField()
  def __str__(self):
    return str(self.id)

class videoSepration(models.Model):
    rawVideo = models.FileField()


class Feedback(models.Model):
  Name = models.CharField(max_length=100) 
  LastName = models.CharField(max_length=100) 

  Email = models.EmailField(max_length=100) 

  Subject = models.CharField(max_length=100) 
  Message = models.CharField(max_length=1000) 
  def __str__(self):
      return str(self.id)


