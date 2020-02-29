from django import forms
from django.core.files.images import get_image_dimensions

from booi_operations.models import Booi, LendBooi
from . import category as ca


class BooiForm(forms.ModelForm):
    booiCategory = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=ca.CHOICES_Category,
    )

    class Meta:
        model = Booi
        fields = [
            'image',
            'booiName',
            'booiAuthor',
            'booiCategory',
            'booiCondition',
            # 'price',
            'search_keyword',
            'brief',
        ]

    def __init__(self, *args, **kwargs):
        super(BooiForm, self).__init__(*args, *kwargs)
        self.fields['image'].label = 'বইয়ের কভার ফটো'
        self.fields['booiName'].label = 'বইয়ের নাম'
        self.fields['booiName'].help_text = 'Do not use "TAKLA" language'
        self.fields['booiAuthor'].label = 'লেখক'
        self.fields['booiCondition'].label = 'বইয়ের হাল'
        self.fields['booiCategory'].label = 'ক্যাটাগরি( একাধিক চিহ্নিত করা যাবে) '
        self.fields['brief'].label = 'সংক্ষিপ্ত বিবরণ'
        self.fields['search_keyword'].label = 'সার্চ কিওয়ার্ড'
        self.fields['search_keyword'].widget.attrs['placeholder'] = ' উপন্যাস, uponnash, novel'
        self.fields['brief'].widget.attrs['placeholder'] = 'বইয়ের ব্যাপারে সংক্ষেপে কিছু লিখুন...'

    def clean_image(self):
        image = self.cleaned_data.get('image')
        w, h = get_image_dimensions(image)
        if h < w:
            raise forms.ValidationError(" ছবির দৈঘ্য অবশ্যই প্রস্থ অপেক্ষা বড় হতে হবে", code='height-width')
        elif h > 3 * w:
            raise forms.ValidationError("ছবির দৈঘ্য অত্যাধিক বড়")
        return image


class LendBooiForm(forms.ModelForm):
    class Meta:
        model = LendBooi
        fields = [
            'securityToken',
        ]


class UpdateBooiForm(forms.ModelForm):
    booiCategory = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=ca.CHOICES_Category,
    )

    class Meta:
        model = Booi
        fields = [
            'image',
            'booiName',
            'booiAuthor',
            'booiCategory',
            'booiCondition',
            'search_keyword',
            'brief',
        ]

    def clean_image(self):
        image = self.cleaned_data.get('image')
        w, h = get_image_dimensions(image)
        if h != 340 or 270 != w:
            raise forms.ValidationError(
                " ছবির দৈঘ্য অবশ্যই 340px  এবং প্রস্থ  অবশ্যই 270px হতে হবে।  ছবির সাইজ ঠিক করতে লিংকে যান: https://www.designhill.com/tools/image-resizer",
                code='height-width')
        return image
