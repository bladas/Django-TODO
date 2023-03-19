from django.db import models
from django.contrib.auth import get_user_model

from base.models import Base

User = get_user_model()


class Image(models.Model):
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.image.url


class TaskStatus(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Task(Base):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(TaskStatus, on_delete=models.PROTECT, related_name='status')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ManyToManyField(Image, related_name='task_images', blank=True)
    executors = models.ManyToManyField(User, related_name="task_executors", blank=True)

    def __str__(self):
        return self.title


class Comments(Base):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_comments")
    comment = models.ForeignKey(
        'Comments', on_delete=models.CASCADE, null=True, blank=True, related_name="comments_on_comments"
    )
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ManyToManyField(Image, related_name='comment_images', blank=True)

    def __str__(self):
        return f"Task pk {self.task.pk} - {self.author}"
