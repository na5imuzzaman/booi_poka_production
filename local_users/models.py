from django.db import models
from django.contrib.auth.models import AbstractUser, User
from allauth.socialaccount.signals import social_account_updated
from allauth.account.signals import user_signed_up
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.urls import reverse
from local_users import semester_choices as sc, years
# from handelbyadmin.models import Notification


class LocalUser(AbstractUser):
    pass


class UserProfile(models.Model):
    owner = models.OneToOneField(LocalUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    #personal
    bio = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    dateOfBirth = models.DateField(null=True, blank=True)
    bg = models.CharField(max_length=6, choices=sc.CHOICES_BG, null=True, blank=True)
    gender = models.CharField(max_length=55, choices=sc.CHOICES_gender, null=True, blank=True)

    #education
    school = models.CharField(max_length=255, null=True, blank=True)
    schoolPassingYear = models.IntegerField(choices=years.YEARS_CHOICES, null=True, blank=True)
    college = models.CharField(max_length=255, null=True, blank=True)
    collegePassingYear = models.IntegerField(null=True, blank=True, choices=years.YEARS_CHOICES)

    #University
    varsityId = models.CharField(max_length=25, null=True, blank=True, unique=True)
    joiningSemester = models.CharField(max_length=255, choices=sc.CHOICES_Semester, null=True, blank=True)
    joiningYear = models.IntegerField(choices=years.YEARS_CHOICES, null=True, blank=True)

    #city
    currentCity = models.CharField(max_length=255, null=True, blank=True)
    homeTown = models.CharField(max_length=255, null=True, blank=True)

    #join_update
    dateJoin = models.DateTimeField(auto_now=False, auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True, auto_now_add=False)

    #notification
    notification = models.IntegerField(default=0)

    def __str__(self):
        return self.owner.username

    def get_absolute_url_profile(self):
        return reverse('profile', kwargs={'username': self.owner.username})

    def get_absolute_url_profile_edit(self):
        return reverse('profile-edit', kwargs={'username': self.owner.username})


# @receiver(pre_save, sender=UserProfile)
# def add_slug(instance, sender, **kwargs):
#     if not instance.slug:
#         instance.slug = slugify(instance.owner.username)

@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    new_m = UserProfile()

    new_m.owner = user
    new_m.save()
    # obj = Notification()
    # obj.to = request.user.username
    # obj.noti_type = 'create_account'
    # obj.save()

