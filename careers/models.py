from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Career(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='careers')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


class Step(models.Model):
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=200)
    order_num = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['order_num']

    def __str__(self):
        return f'{self.career.title} --- {self.title}'


class Material(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='progress')
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'step')

    def __str__(self):
        status = "✓" if self.completed else "✗"
        return f"{self.user.username} — {self.step.title} {status}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    active_career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True, blank=True, related_name='enrolled_users')

    def __str__(self):
        return f"{self.user.username} - {self.active_career}"


class Question(models.Model):
    text = models.CharField(max_length=300)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=200)
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='answers', null=True, blank=True)

    def __str__(self):
        return self.text


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)