from django.urls import path, include
from local_users import views as lv

urlpatterns = [
    path('<username>/', lv.profile_view, name='profile'),
    path('<username>/edit/', lv.profile_edit_view, name='profile-edit'),
]
