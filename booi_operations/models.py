import sys
from django.db import models
from django import forms
from django.utils.text import slugify
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from booi_operations import category, conditions
from local_users.models import UserProfile


def get_uplaod_file_name(booiowner, filename):
    return u'photos/%s/%s/%s' % (booiowner.booiOwner.owner.username, booiowner.booiName, filename)


class Booi(models.Model):
    image = models.ImageField(upload_to=get_uplaod_file_name)
    booiName = models.CharField(max_length=255)
    booiAuthor = models.CharField(max_length=255)
    booiCategory = models.CharField(max_length=255) #choices=category.CHOICES_Category
    booiCondition = models.CharField(max_length=255, choices=conditions.CHOICES_Condition)
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    brief = models.TextField(null=True, blank=True)
    booiOwner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    borrowedTimes = models.IntegerField(default=0)
    acceptByAdmin = models.BooleanField(default=False)
    deleteRequest = models.BooleanField(default=False)
    finally_publish = models.BooleanField(default=False)
    search_keyword = models.CharField(max_length=2055, null=True, blank=True)
    slug = models.SlugField(allow_unicode=True, null=True, blank=True, max_length=20055)

    def save(self, *args, **kwargs):
        if not self.id:
            self.image = self.compressImage(self.image)
        super(Booi, self).save(*args, **kwargs)

    def compressImage(self, image):
        imageTemproary = Image.open(image)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((270, 340))
        try:
            # imageTemproary
            imageTemproaryResized.save(outputIoStream, format='JPEG', quality=90) #format='JPEG'
        except (OSError, FileNotFoundError):
            raise forms.ValidationError('Photo should be JPG or JPGE')
        outputIoStream.seek(0)
        image = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % image.name.split('.')[0],
                                             'image/jpeg', sys.getsizeof(outputIoStream), None)
        return image

    def __str__(self):
        return "%s_%s" % (self.booiOwner.owner.username, self.booiName)

    class Meta:
        ordering = ['-published']
        
    def get_absolute_url_book_details(self):
        return reverse('book-details', kwargs={'slug': self.slug})

    def get_absolute_url_book_edit(self):
        return reverse('update-book', kwargs={'slug': self.slug})


@receiver(post_save, sender=Booi)
def add_slug(instance, sender, **kwargs):
    if not instance.slug:
        slug = instance.booiName.replace(' ', '_')
        # slug = slugify(instance.booiName, allow_unicode=True)
        slug = "%s_%s" % (instance.id, slug)
        instance.slug = slug
        instance.save()


class LendBooi(models.Model):
    borrower = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    thisBooi = models.ForeignKey(Booi, models.CASCADE)
    securityToken = models.CharField(max_length=10, unique=True, null=True, blank=True)
    returnToken = models.CharField(max_length=10, unique=True, null=True, blank=True)
    # {#unique=True#}
    borrowed = models.BooleanField(default=False)
    search_keyword = models.CharField(null=True, blank=True, max_length=2055)
    generateTokenTime = models.DateTimeField(auto_now=True)
    borrowBookTime = models.DateTimeField(blank=True, null=True)
    returnWithin = models.DateTimeField(blank=True, null=True)
    returnBook = models.BooleanField(default=False)
    returnTime = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "%s --> %s" % (self.thisBooi, self.borrower)

    class Meta:
        ordering = ['-borrowBookTime', '-generateTokenTime']


# class WishList(models.Model):
#     wishBook = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     addTime = models.DateTimeField(auto_now=True)

# @receiver(pre_save, sender=LendBooi)
# def add_security_token(instance, *args, **kwargs):
#     instance.securityToken = generate
