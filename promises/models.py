from django.db import models
from django.contrib.auth.models import AbstractUser


class Family(models.Model):
    family_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.family_name


class User(AbstractUser):
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        if self.first_name:
            return self.first_name
        else:
            return self.username


class Promise(models.Model):
    STATUS_DRAFT = 1
    STATUS_REJECTED = 2
    STATUS_PROMISED = 3
    STATUS_FAILED = 4
    STATUS_COMPLETED = 5
    STATUS_REWARDED = 6

    STATUS_CHOICES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_PROMISED, 'Promised'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_REWARDED, 'Rewarded'),
    )

    family = models.ForeignKey(Family, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    status = models.IntegerField(choices=STATUS_CHOICES)
    promise_date = models.DateField()
    dead_line = models.DateField()
    description = models.TextField()

    rewarder = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='promise_created')
    performer = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='promise_assigned')

    reward = models.TextField()
    # reward_url = models.TextField(blank=True, null=True)
    # reward_image = models.ImageField(blank=True, null=True, upload_to='media/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title
