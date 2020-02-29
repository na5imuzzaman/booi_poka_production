from datetime import datetime, timedelta
import secrets, string
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required

from booi_operations.models import Booi, LendBooi
from booi_operations.forms import BooiForm, LendBooiForm, UpdateBooiForm
from local_users.models import LocalUser, UserProfile
from handelbyadmin.models import Notification
from handelbyadmin.forms import ReportToBookOwnerForm, ReportToBorrowerForm


def home_view(request):
    carts = LendBooi.objects.filter(borrower__owner__username__exact=request.user.username, borrowed=True,
                                    returnBook=False)
    book_list = Booi.objects.filter(deleteRequest=False, acceptByAdmin=True)
    topbooks = Booi.objects.filter(deleteRequest=False, acceptByAdmin=True).order_by('borrowedTimes')[:20]

    cnt = Booi.objects.filter(booiOwner__owner__username__exact=request.user.username, deleteRequest=False,
                              acceptByAdmin=True)
    wishlist = Booi.objects.filter(lendbooi__borrower__owner__username__exact=request.user.username,
                                   lendbooi__borrowed=False)

    # for notification start
    notifications = Notification.objects.filter(Q(to=request.user.username) | Q(to='for_all'))[:5]
    noti_cnt = 0

    if request.user.is_authenticated:
        user = UserProfile.objects.get(owner__username__exact=request.user.username)
        noti_cnt = user.notification
    # for notification end

    print(topbooks.count())
    newbooks = book_list[:10]

    if request.method == 'POST':
        if 'data' in request.POST:
            obj = UserProfile.objects.get(owner__username__exact=request.user.username)
            obj.notification = max(0, obj.notification - 5)
            obj.save()

    context = {
        'notifications': notifications,
        'noti_cnt': noti_cnt,
        'newbooks': newbooks,
        'topbooks': topbooks,
        'carts': carts,
        'cnt': cnt,
        'wishlist': wishlist,
    }
    return render(request, 'home/index.html', context)


def book_details_view(request, slug):
    book = Booi.objects.get(slug=slug)
    user = None
    try:
        if request.user.is_staff or request.user.is_superuser:
            book = Booi.objects.get(slug=slug)
        elif request.user.username == book.booiOwner.owner.username:
            book = Booi.objects.get(slug=slug)
        else:
            book = Booi.objects.get(slug=slug, deleteRequest=False, acceptByAdmin=True)
    except (ValueError, TypeError, Booi.DoesNotExist):
        book = None
        raise Http404('LOL')

    # for notification start
    notifications = Notification.objects.filter(Q(to=request.user.username) | Q(to='for_all'))[:5]
    noti_cnt = 0

    if request.user.is_authenticated:
        user = UserProfile.objects.get(owner__username__exact=request.user.username)
        noti_cnt = user.notification
    # for notification end

    if request.user.is_authenticated and request.user.is_active:
        borrowedby = LendBooi.objects.filter(thisBooi=book, borrowed=True, returnBook=False)
        # print(borrowedby[0].borrower.owner.username)
        carts = LendBooi.objects.filter(borrower__owner__username__exact=request.user.username, borrowed=True,
                                        returnBook=False)
        cartbooks = Booi.objects.filter(lendbooi__borrower__owner__username__exact=request.user.username,
                                        lendbooi__borrowed=True,
                                        lendbooi__returnBook=False)
        cnt = Booi.objects.filter(booiOwner__owner__username__exact=request.user.username, deleteRequest=False,
                                  acceptByAdmin=True).count()
        wishlisted = LendBooi.objects.filter(thisBooi=book, borrower__owner__username__exact=request.user.username,
                                             returnBook=False)
        del_wish = LendBooi.objects.filter(borrower__owner__username__exact=request.user.username,
                                           borrowed=False, returnBook=False)

        if request.method == 'POST':
            if request.user.is_staff:
                if request.POST['verifybook'] == 'acceptbyadmin':
                    book.acceptByAdmin = True
                    book.save()
                    return redirect('book-details', slug=book.slug)
                elif request.POST['verifybook'] == 'deletebook':
                    book.delete()
                    return redirect('home')
            elif request.POST['action'] == 'deactive':
                book.deleteRequest = False
                book.save()
                return redirect('book-details', slug=book.slug)
            elif request.POST['action'] == 'removewishlist':
                wishlisted[0].delete()
                return redirect('book-details', slug=book.slug)
            elif request.POST['action'] == 'returntoken':
                obj = LendBooi.objects.get(thisBooi=book,
                                           thisBooi__booiOwner__owner__username__exact=request.user.username,
                                           borrowed=True, returnBook=False)
                alphabet = string.digits + string.ascii_uppercase
                token = ''.join(secrets.choice(alphabet) for i in range(7))
                obj.returnToken = token
                print(obj.returnToken)
                obj.save()
                return redirect('book-details', slug=book.slug)

            elif request.POST['action'] == 'newtoken':
                obj = LendBooi.objects.get(thisBooi=book, borrower__owner__username__exact=request.user.username,
                                           borrowed=False)
                alphabet = string.digits + string.ascii_uppercase
                token = ''.join(secrets.choice(alphabet) for i in range(6))
                obj.securityToken = token
                print(obj.securityToken)
                obj.save()
                return redirect('book-details', slug=book.slug)

            elif request.POST['action'] == 'request':
                form = LendBooi()
                form.borrower = user
                alphabet = string.digits + string.ascii_uppercase
                token = ''.join(secrets.choice(alphabet) for i in range(6))
                form.securityToken = token  # 'ABCDEF'
                form.thisBooi = book
                form.save()
                return redirect('book-details', slug=book.slug)

            elif request.POST['action'] == 'confirm':
                token = request.POST['token']
                print(token)
                objj = LendBooi.objects.filter(thisBooi=book, securityToken=token, borrowed=False)
                print(objj.count())
                if objj.count() == 1:
                    cng = LendBooi.objects.get(thisBooi=book, securityToken=token, borrowed=False)
                    cng.borrowed = True
                    book.available = False
                    book.borrowedTimes = book.borrowedTimes + 1
                    cng.borrowBookTime = datetime.now()
                    cng.returnWithin = datetime.now() + timedelta(days=7)
                    alphabet = string.digits + string.ascii_uppercase
                    token = ''.join(secrets.choice(alphabet) for i in range(9))
                    cng.securityToken = token
                    cng.returnToken = ''.join(secrets.choice(alphabet) for i in range(7))
                    cng.save()
                    book.save()
                    print(cng.borrower.owner.username)
                    print(cng.borrowed)
                    return redirect('book-details', slug=book.slug)
                else:
                    return HttpResponse(
                        '<script>window.alert("False Token. Please, click browser back button to see page content ")</script>')

            elif request.POST['action'] == 'returnToken':
                token = request.POST['return']
                print(token)
                objj = LendBooi.objects.filter(thisBooi=book, returnToken=token, borrowed=True, returnBook=False)
                print(objj.count())
                if objj.count() == 1:
                    cng = LendBooi.objects.get(thisBooi=book, returnToken=token, borrowed=True, returnBook=False)
                    # book.available = True
                    cng.returnTime = datetime.now()
                    cng.returnBook = True
                    alphabet = string.digits + string.ascii_uppercase
                    token = ''.join(secrets.choice(alphabet) for i in range(10))
                    cng.returnToken = token
                    cng.save()
                    # book.save()
                    print(cng.borrower.owner.username)
                    print(cng.borrowed)
                    return redirect('book-details', slug=book.slug)
                else:
                    return HttpResponse(
                        '<script>window.alert("False Token. Please, click browser back button to see page content ")</script>')

            elif request.POST['action'] == 'delete':
                book.deleteRequest = True
                book.save()
                if cnt - 1 < 2:
                    for wish in del_wish:
                        wish.delete()
                return redirect('book-details', slug=book.slug)

            elif request.POST['action'] == 'reportbook':
                form = ReportToBookOwnerForm(request.POST)
                if form.is_valid():
                    n_form = form.save(commit=False)
                    n_form.book = book
                    n_form.report_by = user
                    n_form.status = 'অমীমাংসিত'
                    n_form.save()
                return redirect('book-details', slug=book.slug)

            elif request.POST['action'] == 'reportborrower':
                b_form = ReportToBorrowerForm(request.POST)
                if b_form.is_valid():
                    n_form = b_form.save(commit=False)
                    n_form.book = book
                    n_form.report_to = borrowedby[0].borrower

                    n_form.status = 'অমীমাংসিত'
                    n_form.save()
                return redirect('book-details', slug=book.slug)
    else:
        form = ReportToBookOwnerForm()
        b_form = ReportToBorrowerForm()
        con = {
            'notifications': None,
            'noti_cnt': 0,
            'book': book,
            'form': form,
            'b_form': b_form,
        }
        return render(request, 'details/single-product.html', con)
    # home / book_details.html
    form = ReportToBookOwnerForm()
    b_form = ReportToBorrowerForm()
    context = {
        'notifications': notifications,
        'noti_cnt': noti_cnt,
        'book': book,
        'cnt': cnt,
        'wishlisted': wishlisted,
        'carts': carts,
        'borrowedby': borrowedby,
        'cartbooks': cartbooks,
        'form': form,
        'b_form': b_form,
    }
    return render(request, 'details/single-product.html', context)


@login_required
def book_add_view(request):
    user_info = UserProfile.objects.get(owner__username__exact=request.user.username)
    carts = LendBooi.objects.filter(borrower__owner__username__exact=request.user.username, borrowed=True,
                                    returnBook=False)
    # for notification start
    notifications = Notification.objects.filter(Q(to=request.user.username) | Q(to='for_all'))[:5]

    noti_cnt = 0

    noti_cnt = user_info.notification
    # for notification end

    if request.method == 'POST':
        form = BooiForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.booiOwner = user_info
            new_form.save()
            return redirect('book-details', slug=new_form.slug)
    else:
        form = BooiForm()
    context = {
        'form': form,
        'noti_cnt': noti_cnt,
        'notifications': notifications,
        'user_info': user_info,
        'carts': carts,
    }

    return render(request, 'book/add_book.html', context)


@login_required
def book_update_view(request, slug):
    user_info = UserProfile.objects.get(owner__username__exact=request.user.username)
    carts = LendBooi.objects.filter(borrower__owner__username__exact=request.user.username, borrowed=True,
                                    returnBook=False)
    # for notification start
    notifications = Notification.objects.filter(Q(to=request.user.username) | Q(to='for_all'))[:5]

    noti_cnt = 0

    noti_cnt = user_info.notification
    # for notification end
    ins = Booi.objects.get(slug__exact=slug, acceptByAdmin=False)
    if ins.booiOwner.owner.username == request.user.username or request.user.is_staff:

        if request.method == 'POST':
            form = UpdateBooiForm(request.POST or None, request.FILES or None ,instance=ins)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.save()
                return redirect('book-details', slug=slug)
        else:
            form = UpdateBooiForm(instance=ins)

        context = {
            'form': form,
            'noti_cnt': noti_cnt,
            'notifications': notifications,
            'user_info': user_info,
            'carts': carts,
        }

        return render(request, 'book/add_book.html', context)
    else:
        return HttpResponse('<h1>Access Denied</h1>')


def filter_book(request):

    cnt = Booi.objects.filter(booiOwner__owner__username__exact=request.user.username, deleteRequest=False,
                              acceptByAdmin=True)
    wishlist = Booi.objects.filter(lendbooi__borrower__owner__username__exact=request.user.username,
                                   lendbooi__borrowed=False, acceptByAdmin=True)

    # for notification start
    carts = LendBooi.objects.filter(borrower__owner__username__exact=request.user.username, borrowed=True,
                                    returnBook=False)
    notifications = Notification.objects.filter(Q(to=request.user.username) | Q(to='for_all'))[:5]
    noti_cnt = 0

    if request.user.is_authenticated:
        user = UserProfile.objects.get(owner__username__exact=request.user.username)
        noti_cnt = user.notification
    # for notification end
    print(cnt)
    query = ''
    results = None
    if request.method == 'GET':
        if 'search' in request.GET:
            query = request.GET.get('search')
            results = Booi.objects.filter(
                Q(booiName__icontains=query) | Q(search_keyword__icontains=query) | Q(booiAuthor__icontains=query) | Q(booiCategory__icontains=query) | Q(
                    booiOwner__owner__first_name__icontains=query) ).exclude(
                Q(deleteRequest=True) | Q(acceptByAdmin=False))
        else:
            query = request.GET.get('filter')
            if query is None:
                alphabet = string.digits + string.ascii_uppercase
                token = ''.join(secrets.choice(alphabet) for i in range(20))
                query = token
            elif request.user.is_staff:
                if query == 'review-pending-books':
                    results = Booi.objects.filter(acceptByAdmin=False)
                elif query == 'review-delete-request':
                    results = Booi.objects.filter(deleteRequest=True)

            elif query == 'all-book':
                results = Booi.objects.filter(deleteRequest=False, acceptByAdmin=True)
            elif query == 'my-books':
                results = Booi.objects.filter(deleteRequest=False,
                                              booiOwner__owner__username__exact=request.user.username,
                                              acceptByAdmin=True)
            elif query == 'deactivated-books':
                results = Booi.objects.filter(booiOwner__owner__username__exact=request.user.username,
                                              deleteRequest=True)
            elif query == 'pending-books':
                results = Booi.objects.filter(booiOwner__owner__username__exact=request.user.username,
                                              acceptByAdmin=False)
            else:
                results = Booi.objects.filter(Q(booiCategory__icontains=query), deleteRequest=False, acceptByAdmin=True)

    # elif request.method == 'POST':
    #     query = request.POST.get('ftext')
    #     if query == 'review-pending-books':
    #         results = Booi.objects.filter(acceptByAdmin=False)
    #     elif query == 'review-delete-request':
    #         results = Booi.objects.filter(deleteRequest=True)

    paginator = Paginator(results, 6)
    page_number = request.GET.get('page')
    results = paginator.get_page(page_number)

    context = {
        'notifications': notifications,
        'noti_cnt': noti_cnt,
        'results': results,
        'carts': carts,
        'query': query,
        'cnt': cnt,
        'wishlist': wishlist,
        'paginator': paginator
    }
    return render(request, 'category/shop-grid.html', context)


def wish_list(request):
    results = Booi.objects.filter(deleteRequest=False, lendbooi__borrower__owner__username__exact=request.user.username,
                                  lendbooi__borrowed=False, acceptByAdmin=True)
    carts = LendBooi.objects.filter(borrower__owner__username__exact=request.user.username, borrowed=True,
                                    returnBook=False)
    # for notification start
    notifications = Notification.objects.filter(Q(to=request.user.username) | Q(to='for_all'))[:5]
    noti_cnt = 0

    if request.user.is_authenticated:
        user = UserProfile.objects.get(owner__username__exact=request.user.username)
        noti_cnt = user.notification
    # for notification end

    context = {
        'results': results,
        'carts': carts,
        'query': 'wishlist',
        'notifications': notifications,
        'noti_cnt': noti_cnt,
    }
    return render(request, 'category/shop-grid.html', context)
