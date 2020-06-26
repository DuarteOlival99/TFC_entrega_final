from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta, date
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField

# Create your models here.

GENDER_CHOICES = (
    ("male", "male"),
    ("female", "female"),
)


class Client(models.Model):
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=254, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES,
                              max_length=254, blank=True, default=GENDER_CHOICES[0])
    birthday = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True, default="Portugal")
    phone = models.CharField(max_length=12, blank=False)
    nIF = models.CharField(max_length=9, blank=True, validators=[RegexValidator(
        regex='^.{9}$', message='Length has to be 9', code='nomatch')])
    balance = models.FloatField(blank=True, default=0.0)
    debt = models.IntegerField(blank=True, default=0)
    discount = models.IntegerField(blank=True, default=0)
    notes = models.TextField(default="", blank=True)

    def __str__(self):
        """ String para representar o objeto MyModelName (no site Admin)."""
        return self.name

    def get_absolute_url(self):
        return f"/clients/{self.id}/"


class Profile(models.Model):
    """ modelo do staff """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=30, blank=True, default="")
    lastName = models.CharField(max_length=30, blank=True, default="")
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=30, blank=True, default="")
    birthday = models.DateField(null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    driver = models.BooleanField(blank=True, default=False)
    instructor = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return f'{self.user.username}'

    def delete_user(self):
        self.user.delete()

    def get_driver(self):
        if self.driver == True:
            return "yes"
        elif self.driver == False:
            return "no"
        else:
            return "None"

    def get_instructor(self):
        if self.instructor == True:
            return "yes"
        elif self.instructor == False:
            return "no"
        else:
            return "None"

    def get_absolute_url(self):
        return f"/profile/edit/{self.id}/"


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Gender(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        """ String para representar o objeto MyModelName (no site Admin)."""
        return self.name


class Driver(models.Model):
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=254, blank=True)

    def __str__(self):
        """ String para representar o objeto MyModelName (no site Admin)."""
        return self.name


class Modalidade(models.Model):
    name = models.CharField(blank=True, max_length=32, null=False)
    price = models.FloatField(blank=True, null=True)

    def __str__(self):
        """ String para representar o objeto MyModelName (no site Admin)."""
        return self.name

    def getName(self):
        return self.name


class Boat(models.Model):
    name = models.CharField(blank=True, max_length=32, null=False)

    def __str__(self):
        """ String para representar o objeto MyModelName (no site Admin)."""
        return self.name


class Instructor(models.Model):
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=254, blank=True)

    def __str__(self):
        """ String para representar o objeto MyModelName (no site Admin)."""
        return self.name


def get_clients():
    return Client.objects.all()


class Event(models.Model):
    client = models.ForeignKey(
        Client, null=False, blank=False, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=datetime.now())
    end_time = models.DateTimeField(default=datetime.now())
    time = models.IntegerField(default=0, blank=True)
    driver = models.ForeignKey(
        Profile, null=False, on_delete=models.CASCADE, blank=True, related_name='driverr')
    instructor = models.ForeignKey(
        Profile, null=False, on_delete=models.CASCADE, blank=True, related_name='instructorr')
    boat = models.ForeignKey(
        Boat, null=False, on_delete=models.CASCADE, blank=True)
    modality = models.ForeignKey(
        Modalidade, null=False, on_delete=models.CASCADE, default="")
    price = models.FloatField(blank=True, default=0)
    payed = models.BooleanField(default=False, blank=False)
    grades = models.TextField(blank=True, default="")

    def __str__(self):
        """ String para representar o objeto MyModelName (no site Admin)."""
        return self.client.name

    def getId(self):
        return self.id

    def get_absolute_url(self):
        return f"/event/{self.id}/edit/"

    def get_notes(self):
        if self.grades.__sizeof__ == 0:
            return "None"
        else:
            return self.grades

    def get_payed(self):
        if self.payed == True:
            return "yes"
        elif self.payed == False:
            return "no"

    def hour_auto(self):
        self.end_time = django.utils.timezone.now()
        return self

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.client.name} {self.start_time} </a>'
