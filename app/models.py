import json

from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from datetime import datetime
# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField()
    slug = models.SlugField(max_length=200, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class TaskDate(models.Model):
   task = models.ForeignKey(Task, on_delete=models.CASCADE)
   date = models.DateField(null=True, blank=True)

class History(models.Model):
   history = models.TextField(default='{}')




# def task_handler(sender, instance, **kwargs):
#     print("inside task handler")
#     print(instance.name)
#     print(instance.description)
#
# pre_save.connect(task_handler, sender=Task)


@receiver(pre_save, sender=Task)
def task_handler(sender, instance, **kwargs):
    print("pre save using decorator")
    print(instance.name)
    print(instance.description)
    print(slugify(instance.name)) #slug ex
    instance.slug = slugify(instance.name) #slug ex


@receiver(post_save, sender=Task)
def task_handler_post(sender, instance, **kwargs):
    TaskDate.objects.create(task=instance, date=datetime.now())

@receiver(pre_delete, sender=Task)
def task_handler_pre_delete(sender, instance, **kwargs):
    data = {'name':instance.name, 'descripton':instance.description, 'slug':instance.slug}
    data = json.dumps(data)
    History.objects.create(history=data)