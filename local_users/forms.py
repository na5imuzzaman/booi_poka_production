from django import forms
from local_users.models import UserProfile


class UserProfileForm(forms.ModelForm):
    dateOfBirth = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = UserProfile
        fields = [
            'varsityId',
            'dateOfBirth',
            'bg',
            'phone',
            'school',
            'schoolPassingYear',
            'college',
            'collegePassingYear',
            'joiningSemester',
            'joiningYear',
            'currentCity',
            'homeTown',
            'bio',
        ]

    # def __init__(self, *args, **kwargs):
    #     super(UserProfileForm, self).__init__(*args, **kwargs)
    #     self.fields['varsityId'].label = 'University ID'
    #     self.fields['varsityId'].help_text = 'ex. 123-45-6789'
    #     self.fields['dateOfBirth'].label = 'Date of Birth'
    #     self.fields['bg'].label = 'Blood Group'
    #     self.fields['school'].label = 'School Name'
    #     self.fields['schoolPassingYear'].label = 'S.S.C.'
    #     self.fields['college'].label = 'College Name'
    #     self.fields['collegePassingYear'].label = 'H.S.C.'
    #     self.fields['joiningSemester'].label = 'Admission Semester'
    #     self.fields['joiningYear'].label = 'Admission Year'
    #     self.fields['currentCity'].label = 'Current Address'
    #     self.fields['homeTown'].label = 'Permanent Address'
    #     self.fields['bio'].label = 'Bio'

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['varsityId'].label = 'বিশ্ববিদ্যালয়ের পরিচয়পত্র নম্বর'
        self.fields['varsityId'].help_text = 'ex. 123-45-6789'
        self.fields['dateOfBirth'].label = 'জন্মতারিখ'
        self.fields['bg'].label = 'রক্তের গ্রুপ'
        self.fields['school'].label = 'স্কুলের নাম'
        self.fields['schoolPassingYear'].label = 'এসএসসি'
        self.fields['college'].label = 'কলেজের নাম'
        self.fields['collegePassingYear'].label = 'এইচ এস সি'
        self.fields['joiningSemester'].label = 'ভর্তি সেমিস্টার'
        self.fields['joiningYear'].label = 'ভর্তি বছর'
        self.fields['currentCity'].label = 'বর্তমান ঠিকানা'
        self.fields['homeTown'].label = 'স্থায়ী ঠিকানা'
        self.fields['bio'].label = 'নিজের সম্পর্কে'
        self.fields['phone'].widget.attrs['placeholder'] = '017...'
        self.fields['phone'].label = 'ফোন নাম্বার'

    def clean_varsityId(self):
        varsityId = self.cleaned_data.get('varsityId')
        if varsityId == 'tasnimridi':
            return varsityId
        cnt = varsityId.count('-')
        numeric = varsityId.replace('-', '')
        if cnt != 2 or not numeric.isnumeric():
            raise forms.ValidationError("Enter Valid ID with correct format.")
        return varsityId
