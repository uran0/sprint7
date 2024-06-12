from django.db import models
from django.utils.timezone import now
from account.models import User

class Status(models.Model):
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.status
    
class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Priority(models.Model):
    priority = models.BooleanField(default=False)

    def __str__(self):
        return "Alta" if self.priority else "Baja"

    
class Task(models.Model):
    name = models.CharField(max_length=150)
    expire_date = models.DateField(blank=False, null=False, default=now)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)

    def __str__(self):
        return self.name