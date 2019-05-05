from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.core.mail import send_mail
from django.utils.dates import MONTHS
from datetime import date


class User(AbstractUser):
    first_name = models.CharField(verbose_name="First name", max_length=255)
    last_name = models.CharField(verbose_name="Last name", max_length=255)
    country = models.CharField(verbose_name="Country name", max_length=255)
    city = models.CharField(verbose_name="City name", max_length=255)
    email = models.EmailField(verbose_name="Email", max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} {}' .format(self.first_name, self.last_name)

#signal used for is_active=False to is_active=True
@receiver(pre_save, sender=User, dispatch_uid='active')
def active(sender, instance, **kwargs):
    try:
        if instance.is_active and User.objects.filter(pk=instance.pk, is_active=False).exists():
            subject = 'Your account is activated'
            mesagge = '%s your account is now active. Your username is: %s. Click the link to log in your accout https://emeupci.com/accounts/login/' %(instance.first_name, instance.username)
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, mesagge, from_email, [instance.email], fail_silently=False)
    except:
        print("Something went wrong, please try again.")
#signal to send an email to the admin when a user creates a new account
@receiver(post_save, sender=User, dispatch_uid='register')
def register(sender, instance, **kwargs):
    try:
        if kwargs.get('created', False):
            subject = "Verificatión of the %s 's account" %(instance.username)
            mesagge = '%s, %s just registered in www.emeupci.com. Click the link to activate him https://emeupci.com/admin/. ' %(instance.first_name, instance.last_name)
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, mesagge, from_email, [from_email], fail_silently=False)
    except:
        print("Something went wrong, please try again.")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.user.username

    def save(self, force_insert=False, force_update=False, using=None):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 250 or img.width > 250:
            output_size = (250, 250)
            img.thumbnail(output_size)
            img.save(self.image.path)



def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)


class Area(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Country(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    access_challenge = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Post(models.Model):
    name = models.CharField('Church name:', max_length=100)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    social = models.URLField(max_length=255, blank=True)
    phone = models.CharField(max_length=255)
    website = models.URLField(max_length=255, blank=True)
    date_posted = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Added by: ', null=True, blank=True)


    def __str__(self):
        return '%s' % self.name

class Report(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Created by: ')
    month = models.DateField(default=date.today)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    new_ministers = models.IntegerField('How many new Ministers <br> in Training?', default=0)
    dis_course = models.IntegerField('How many are in Discipleship Courses?', default=0)
    licenced_ministers = models.IntegerField('How many newly Licensed Ministers?', default=0)
    upgrade_licence = models.IntegerField('How many Upgraded Licenses?', default=0)
    preaching_place = models.IntegerField('How many New Preaching Places?', default=0)
    new_churches = models.IntegerField('How many New Churches?', default=0)
    water_baptism = models.IntegerField('How many were Baptized in Jesus Name?', default=0)
    holy_ghost = models.IntegerField('How many Received <br> the Holy Ghost?', default=0)
    constituents = models.IntegerField('Current Constituents:', default=0)
    total_holy_ghost = models.IntegerField('Total Filled with the Holy Ghost:', default=0)
    total_baptized = models.IntegerField('Total Baptized in Jesus Name:', default=0)

    def __str__(self):
        return '{}'.format(self.area)


    def get_absolute_url(self):
        return reverse('users:report_list')
