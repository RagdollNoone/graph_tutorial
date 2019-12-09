from datetime import timezone

from django.db import models

# Create your models here.
class Events(models.Model):
    Id = models.IntegerField(primary_key=True)
    Subject = models.CharField(max_length=255)
    Organizer = models.CharField(max_length=255)
    Organizeraddress = models.CharField(max_length=255)
    Start = models.DateTimeField()
    End = models.DateTimeField()
    Location = models.CharField(max_length=255)
    Mailsend = models.IntegerField(default='0')
    Graphid=models.CharField(max_length=255)
    def __str__(self):
        return "%d:%s:%s:%s:%s:%s:%s:%d:%s"%(self.Id,self.Subject,self.Organizer,self.Organizeraddress,self.Start,self.End,self.Location,self.Mailsend,self.Graphid)

    class Meta:
        db_table = "events"

class Attendees(models.Model):
    Id = models.IntegerField(primary_key=True)
    Eventid = models.IntegerField()
    Name = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    Isattend = models.IntegerField(default='0')
    Meetingtime = models.DateTimeField()
    Attendtime = models.DateTimeField()
    def __str__(self):
        return "%d:%d:%s:%s:%d:%s:%s"%(self.Id,self.Eventid,self.Name,self.Address,self.Isattend,self.Meetingtime,self.Attendtime)

    class Meta:
        db_table = "attendees"

class User(models.Model):
    Id = models.IntegerField(primary_key=True)
    Openid = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    Passwd=models.CharField(max_length=255)
    Name = models.CharField(max_length=255)
    Group = models.CharField(max_length=255)
    def __str__(self):
        return "%d:%s:%s:%s:%s"%(self.Id,self.Openid,self.Address,self.Passwd,self.Name,self.Group)

    class Meta:
        db_table = "user"