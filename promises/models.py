from django.db import models
from django.contrib.auth.models import AbstractUser

class Family(models.Model):
    family_name = models.CharField(max_length=50)

    def __str__(self):
        return self.family_name

class User(AbstractUser):
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True)
    # family_id = models.IntegerField(null=True)
    # is_child = models.BooleanField(default=False)

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

    STATUS_CHOICES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_PROMISED, 'Promised'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_COMPLETED, 'Completed'),
    )

    # family_id = models.IntegerField()
    family = models.ForeignKey(Family, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    status = models.IntegerField(choices=STATUS_CHOICES)
    promise_date = models.DateField()
    dead_line = models.DateField()
    description = models.TextField()

    rewarder = models.ForeignKey(User, on_delete=models.PROTECT, related_name='promise_created')
    performer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='promise_assigned')

    reward = models.TextField()
    # reward_url = models.TextField(blank=True, null=True)
    # reward_image = models.ImageField(blank=True, null=True, upload_to='media/')

    def __str__(self):
        return self.title


# class PromiseDetail(models.Model):
#     promise_id = models.IntegerField()

# class Person(models.Model):
#     family_id = models.IntegerField()
#     first_name = models.CharField(max_length=20)
#     last_name = models.CharField(max_length=20)
#     mail_address = models.CharField(max_length=100)
#     is_child = models.BooleanField(default=False)

#     def __str__(self):
#         return self.first_name + ' ' + self.last_name
