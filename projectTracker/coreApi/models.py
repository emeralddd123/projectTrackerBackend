from django.db import models
from django.conf.global_settings import AUTH_USER_MODEL as User
import uuid, random
# Create your models here.

def randomize(title):
    ran = random.randint(1000000,10000000)
    return str(ran+title)

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    )
    
    STATUS_CHOICES = (
        ('UNCOMPLETED', 'uncompleted'),
        ('COMPLETED', 'completed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True,unique=True,editable=False)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    date = models.DateField()
    remind = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.title 
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = randomize(self.title)
        super(Task, self).save(*args, **kwargs)