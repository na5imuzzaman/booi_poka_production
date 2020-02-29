from django.shortcuts import render, HttpResponse, get_object_or_404, Http404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from local_users.models import UserProfile, LocalUser
from local_users.forms import UserProfileForm
from booi_operations.models import Booi, LendBooi
from handelbyadmin.models import Notification


@login_required
def profile_edit_view(request, username):
    user = None
    # for notification start
    notifications = Notification.objects.filter(Q(to=request.user.username) | Q(to='for_all'))[:5]
    noti_cnt = 0

    if request.user.is_authenticated:
        user = UserProfile.objects.get(owner__username__exact=request.user.username)
        noti_cnt = user.notification
    # for notification end
    if request.user.username == username:
        cnt = Booi.objects.filter(booiOwner__owner__username__exact=request.user.username, deleteRequest=False)
        carts = LendBooi.objects.filter(borrower__owner__username__exact=request.user.username, borrowed=True,
                                        returnBook=False)
        ins = UserProfile.objects.get(owner__username__exact=username)
        if request.method == 'POST':
            form = UserProfileForm(request.POST or None,  instance=ins)
            if form.is_valid():
                form.save()
                return redirect('../')
        else:
            form = UserProfileForm(instance=ins)

        context = {
            'form': form,
            'carts': carts,
            'notifications': notifications,
            'noti_cnt': noti_cnt,
            'user_info': user,
        }
        return render(request, 'user_account/user_account_edit.html', context)
    else:
        raise PermissionDenied()


def profile_view(request, username):
    try:
        profile = UserProfile.objects.get(owner__username__exact=username)
    except (TypeError, OverflowError, TypeError, UserProfile.DoesNotExist):
        raise Http404()

    # for notification start
    notifications = Notification.objects.filter(Q(to=request.user.username) | Q(to='for_all'))[:5]
    noti_cnt = 0

    if request.user.is_authenticated:
        user = UserProfile.objects.get(owner__username__exact=request.user.username)
        noti_cnt = user.notification
    # for notification end
    books = Booi.objects.filter(booiOwner__owner__username__exact=username)
    borrowed = LendBooi.objects.filter(borrower__owner__username__exact=username)
    carts = LendBooi.objects.filter(borrower__owner__username__exact=request.user.username, borrowed=True,
                                    returnBook=False)

    context = {
        'profile': profile,
        'books': books,
        'borrowed': borrowed,
        'carts': carts,
        'notifications': notifications,
        'noti_cnt': noti_cnt,
    }

    return render(request, 'user_account/user_account_view.html', context)





