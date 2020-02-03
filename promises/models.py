from django.db import models


class Promise(models.Model):
    family_id = models.IntegerField(blank=True, null=True, default=0)
    title = models.CharField(max_length=100)
    promise_date = models.DateTimeField()
    dead_line = models.DateTimeField(blank=True, null=True)
    description = models.TextField()

    performer_person_id = models.IntegerField(blank=True, null=True, default=0)
    rewarder_person_id = models.IntegerField(blank=True, null=True, default=0)

    reward = models.TextField(blank=True, null=True)
    reward_url = models.TextField(blank=True, null=True)
    reward_image = models.ImageField(blank=True, null=True, upload_to='media/')

    def __str__(self):
        return self.title


# class PromiseDetail(models.Model):
#     promise_id = models.IntegerField()


class Family(models.Model):
    family_name = models.CharField(max_length=50)

    def __str__(self):
        return self.family_name


class Person(models.Model):
    family_id = models.IntegerField(blank=True, null=True, default=0)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    mail_address = models.CharField(max_length=100, blank=True, null=True)
    is_child = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
