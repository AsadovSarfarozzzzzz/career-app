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

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    title = models.CharField(max_length=200)
    icon = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.category.title} --> {self.title}'
    

class Career(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='careers')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='careers')
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

class Topic(models.Model):
    step = models.ForeignKey(
        Step, on_delete=models.CASCADE, 
        related_name='topics'
    )
    title = models.CharField(max_length=200)
    order_num = models.IntegerField(default=0)
    content = models.TextField(blank=True)

    class Meta:
        ordering = ['order_num']

    def __str__(self):
        return f"{self.step.title} → {self.title}"

class Page(models.Model):
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE,
        related_name='pages'
    )
    order_num = models.IntegerField(default=0)
    content = models.TextField(blank=True)

    class Meta:
        ordering = ['order_num']

    def __str__(self):
        return f"{self.topic.title} → страница {self.order_num}"

class TopicProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_progress')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='progress')
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'topic')

    def __str__(self):
        return f"{self.user.username} — {self.topic.title}"

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
    xp = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    last_activity = models.DateField(null=True, blank=True)

    @property
    def level(self):
        return self.xp // 100 + 1

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