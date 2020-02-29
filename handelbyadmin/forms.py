from django import forms
from handelbyadmin.models import Faq, Notification, ReportToBookOwner, ReportToBorrower


class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = [
            'question',
            'answer',
        ]


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = [
            'to',
            'noti_type',
            'noti_body',
        ]

    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
        self.fields['noti_body'].label = 'Notification Body'
        self.fields['noti_type'].label = 'Notification Type'
        self.fields['noti_body'].help_text = 'For push this text, you need to choose "text" as Notification Type'


class ReportToBookOwnerForm(forms.ModelForm):
    class Meta:
        model = ReportToBookOwner
        fields = [
            'subject',
            'message',
        ]

    def __init__(self, *args, **kwargs):
        super(ReportToBookOwnerForm, self).__init__(*args, **kwargs)
        self.fields['subject'].label = 'বিষয়'
        self.fields['message'].label = ' বিস্তারিত বর্ণনা'
        self.fields['message'].widget.attrs['placeholder'] = ' আপনার সমস্যা বর্ণনা করুন...'


class ReportToBorrowerForm(forms.ModelForm):
    class Meta:
        model = ReportToBorrower
        fields = [
            'subject',
            'message',
        ]

    def __init__(self, *args, **kwargs):
        super(ReportToBorrowerForm, self).__init__(*args, **kwargs)
        self.fields['subject'].label = 'বিষয়'
        self.fields['message'].label = ' বিস্তারিত বর্ণনা'
        self.fields['message'].widget.attrs['placeholder'] = ' আপনার সমস্যা বর্ণনা করুন...'


class AdminReportToBookOwnerForm(forms.ModelForm):
    class Meta:
        model = ReportToBookOwner
        fields = [
            'solution'
        ]

    def __init__(self, *args, **kwargs):
        super(AdminReportToBookOwnerForm, self).__init__(*args, **kwargs)
        self.fields['solution'].label = 'সল্যুশন'


class AdminReportToBorrowerForm(forms.ModelForm):
    class Meta:
        model = ReportToBorrower
        fields = [
            'solution'
        ]

    def __init__(self, *args, **kwargs):
        super(AdminReportToBorrowerForm, self).__init__(*args, **kwargs)
        self.fields['solution'].label = 'সল্যুশন'
