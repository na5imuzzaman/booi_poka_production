from django.urls import path, include
from django.views.generic import TemplateView
from handelbyadmin import views as hv


urlpatterns = [
    path('faq/', hv.faq_view, name="faq-view"),
    path('faq/add-faq/', hv.add_faq_view, name="add-faq"),
    path('notification/push-notification/', hv.push_notification_view, name='push-notification'),
    path('our-story/', hv.our_story_view, name='our-story'),
    path('contact-info/', hv.contact_view, name='contact-info'),
    path('report_details/', hv.report_details_view, name='report-details'),
    path('notifications/', hv.all_notification_view, name='all-notification'),
    # path('', TemplateView.as_view(template_name='help.html'), name='help-section'),
]