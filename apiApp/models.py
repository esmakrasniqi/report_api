from django.db import models
from datetime import datetime
from django.urls import reverse,reverse_lazy
# Create your models here.
class Task(models.Model):
    taskId=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100,null=False)
    description=models.TextField(max_length=200)
    date=models.DateField(auto_now_add=True)
    
    def __str__(self):
       return self.name
    
    def get_absolute_url(self):
        return reverse('task_list',args=(str(self.id)))
