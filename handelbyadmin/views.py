from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from handelbyadmin.forms import Faq, FaqForm, Notification, NotificationForm, ReportToBookOwner, ReportToBorrower, \
    AdminReportToBorrowerForm, AdminReportToBookOwnerForm
from booi_operations.models import LendBooi, UserProfile


def faq_view(request):
    # for notification start
    notifications = Notification.objects.filter(Q(to=request.user.username) | Q(to='for_all'))[:5]
    noti_cnt = 0

    if request.user.is_authenticated:
        user = UserProfile.objects.get(owner__username__exact=request.user.username)
        noti_cnt = user.notification
    # for notification end
    carts = LendBooi.objects.filter(borrower__owner__username__exact=request.user.username, borrowed=True,
                                    returnBook=False)
    faqs = Faq.objects.all()
    context = {
        'faqs': faqs,
        'carts': carts,
        'notifications': notifications,
        'noti_cnt': noti_cnt,
    }
    return render(request, 'faq/faq.html', context)


@staff_member_required
def add_faq_view(request):
    user = UserProfile.objects.get(owner__username__exact=request.user.username)
    carts = LendBooi.objects.filter(borrower__owner__username__exact=request.user.username, borrowed=True,
                                    returnBook=False)
    # for notification start
    notifications = Notification.objects.filter(Q(to=request.user.username) | Q(to='for_all'))[:5]
    noti_cnt = 0

    if request.user.is_authenticated:
        user = UserProfile.objects.get(owner__username__exact=request.user.username)
        noti_cnt = user.notification
    # for notification end

    if request.method == 'POST':
        form = FaqForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.added_by = user
            new_form.save()
            return redirect("faq-view")
    form = FaqForm()
    context = {
        'carts': carts,
        'form': form,
        'notifications': notifications,
        'noti_cnt': noti_cnt,
    }
    return render(request, 'faq/add-faq.html', context)


@staff_member_required
def push_notification_view(request):
    # for notification start
    notifications = Notification.objects.filter(Q(to=request.user.username) | Q(to='for_all'))[:5]
    noti_cnt = 0

    if request.user.is_authenticated:
        user = UserProfile.objects.get(owner__username__exact=request.user.username)
        noti_cnt = user.notification
    # for notification end
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            users = UserProfile.objects.all()
            for user in users:
                user.notification += 1
                user.save()

    form = NotificationForm()
    context = {
        'form': form,
        'notifications': notifications,
        'noti_cnt': noti_cnt,
    }
    return render(request, 'push_notification/push-notification.html', context)


def our_story_view(request):
    # for notification start
    carts = LendBooi.objects.filter(borrower__owner__username__exact=request.user.username, borrowed=True,
                                    returnBook=False)
    notifications = Notification.objects.filter(Q(to=request.user.username) | Q(to='for_all'))[:5]
    noti_cnt = 0

    if request.user.is_authenticated:
        user = UserProfile.objects.get(owner__username__exact=request.user.username)
        noti_cnt = user.notification
    # for notification end

    context = {
        'carts': carts,
        'notifications': notifications,
        'noti_cnt': noti_cnt,
    }
    return render(request, 'about.html', context)


def contact_view(request):
    carts = LendBooi.objects.filter(borrower__owner__username__exact=request.user.username, borrowed=True,
                                    returnBook=False)
    # for notification start
    notifications = Notification.objects.filter(Q(to=request.user.username) | Q(to='for_all'))[:5]
    noti_cnt = 0

    if request.user.is_authenticated:
        user = UserProfile.objects.get(owner__username__exact=request.user.username)
        noti_cnt = user.notification
    # for notification end

    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        fake_sub = "Got a new mail from " + name
        admin_email = 'nasimuzzaman15-1127@diu.edu.bd'
        body = render_to_string('response_email.html', {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
        })
        email = EmailMessage(fake_sub, body, to=[admin_email], reply_to=[email])
        email.send()
        return render(request, 'redirect.html', {})

    context = {
        'carts': carts,
        'noti_cnt': noti_cnt,
        'notifications': notifications,
    }
    return render(request, 'contact.html', context)


@staff_member_required
def report_details_view(request):
    user_report = ReportToBookOwner.objects.all()
    owner_report = ReportToBorrower.objects.all()

    paginator1 = Paginator(user_report, 100)
    paginator2 = Paginator(owner_report, 100)
    page_number1 = request.GET.get('page')
    page_number2 = request.GET.get('pages')
    user_report = paginator1.get_page(page_number1)
    owner_report = paginator2.get_page(page_number2)

    if request.method == 'POST':
        if 'reportsolution' in request.POST:
            idd = request.POST['reportsolution']
            ins = get_object_or_404(ReportToBookOwner, id=int(idd))
            rbookform = AdminReportToBookOwnerForm(request.POST, instance=ins)
            if rbookform.is_valid():
                n_rbookform = rbookform.save(commit=False)
                n_rbookform.status = 'মীমাংসিত'
                n_rbookform.investigator = request.user
                n_rbookform.save()

        elif 'reportbook' in request.POST:
            idd = request.POST['reportbook']
            ins = get_object_or_404(ReportToBorrower, id=int(idd))

            rborrowerform = AdminReportToBorrowerForm(request.POST, instance=ins)
            if rborrowerform.is_valid():
                n_rborrowerform = rborrowerform.save(commit=False)
                n_rborrowerform.status = 'মীমাংসিত'
                n_rborrowerform.investigator = request.user
                n_rborrowerform.save()

    rbookform = AdminReportToBookOwnerForm()
    rborrowerform = AdminReportToBorrowerForm()
    context = {
        'user_report': user_report,
        'owner_report': owner_report,
        'rbookform': rbookform,
        'rborrowerform': rborrowerform,
        'paginator1': paginator1,
        'paginator2': paginator2,
    }
    return render(request, 'report_view/report_summary.html', context)


@login_required
@require_http_methods(["GET"])
def all_notification_view(request):
    carts = LendBooi.objects.filter(borrower__owner__username__exact=request.user.username, borrowed=True,
                                    returnBook=False)

    user = UserProfile.objects.get(owner__username__exact=request.user.username, owner__is_active=True)
    mynotifications = Notification.objects.filter(Q(to=request.user.username) | Q(to='for_all'), created_time__gte=user.owner.date_joined)

    paginator = Paginator(mynotifications, 30)
    page_number = request.GET.get('page')
    mynotifications = paginator.get_page(page_number)

    user.notification = max(0, user.notification-30)
    user.save()

    context = {
        'notificationss': mynotifications,
        'notifications': mynotifications[:5],
        'noti_cnt': 0,
        'paginator': paginator,
        'carts': carts,
    }
    return render(request, 'push_notification/all_notification.html', context)