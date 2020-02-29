from django.contrib import admin
from handelbyadmin.models import Faq, Notification, ReportToBookOwner, ReportToBorrower


admin.site.register(Faq)
admin.site.register(Notification)
admin.site.register(ReportToBookOwner)
admin.site.register(ReportToBorrower)
