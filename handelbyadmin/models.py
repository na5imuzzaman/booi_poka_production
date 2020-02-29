from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from tinymce.models import HTMLField

from local_users.models import UserProfile, LocalUser
from booi_operations.models import Booi, LendBooi
from handelbyadmin import notification_type as nt


class Faq(models.Model):
    question = models.CharField(max_length=2055)
    answer = models.TextField()
    added_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s --> %s" % (self.added_by.owner.username, self.question)

    class Meta:
        ordering = ['-add_time']


class Notification(models.Model):
    to = models.CharField(max_length=255, choices=nt.CHOICES_notification_to)
    book = models.ForeignKey(Booi, on_delete=models.CASCADE, null=True, blank=True)
    noti_type = models.CharField(max_length=255, choices=nt.CHOICES_notification_type)
    # noti_body = models.TextField(null=True, blank=True)
    noti_body = HTMLField(null=True, blank=True)
    read = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s --> %s" %(self.to, self.noti_type)

    class Meta:
        ordering = ['-created_time']


@receiver(post_save, sender=Booi)
def add_notification(instance, sender, **kwargs):
    if instance.acceptByAdmin and not instance.finally_publish:
        instance.finally_publish = True
        obj = Notification()
        noti_plus = UserProfile.objects.get(owner__username__exact=instance.booiOwner.owner.username)
        obj.to = instance.booiOwner.owner.username
        obj.book = instance
        obj.noti_type = 'published_book'
        noti_plus.notification += 1
        instance.save()
        noti_plus.save()
        obj.save()


@receiver(post_save, sender=LendBooi)
def available_alert(instance, sender, **kwargs):
    if instance.returnBook is True and instance.thisBooi.available is False:
        booi = Booi.objects.get(slug__exact=instance.thisBooi.slug)
        booi.available = True
        booi.save()
        userlist = UserProfile.objects.filter(lendbooi__thisBooi=booi, lendbooi__borrowed=False)

        for user in userlist:
            obj = Notification()
            obj.to = user.owner.username
            user.notification += 1
            user.save()
            obj.book = booi
            obj.noti_type = 'available_alert'
            obj.save()


class ReportToBookOwner(models.Model):
    book = models.ForeignKey(Booi, on_delete=models.CASCADE)
    report_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    report_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=55)
    message = models.TextField()
    subject = models.CharField(max_length=555)
    investigator = models.ForeignKey(LocalUser, on_delete=models.CASCADE, null=True)
    solution = models.TextField(null=True)

    def __str__(self):
        return "%s ---> %s" % (self.report_by, self.book)

    class Meta:
        ordering = ['-report_time']


class ReportToBorrower(models.Model):
    book = models.ForeignKey(Booi, on_delete=models.CASCADE)
    report_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    report_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=55, choices=nt.CHOICES_status)
    message = models.TextField()
    solution = models.TextField(null=True)
    subject = models.CharField(max_length=555)
    investigator = models.ForeignKey(LocalUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "%s --> %s" % (self.book, self.report_to)

    class Meta:
        ordering = ['-report_time']