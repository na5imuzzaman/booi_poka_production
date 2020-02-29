from django.urls import path
from booi_operations import views as bv

urlpatterns = [
    path('', bv.home_view, name="home"),
    path('book/add-book/', bv.book_add_view, name="add-book"),
    path('book/<slug>/', bv.book_details_view, name="book-details"),
    path('book/<slug>/update-info/', bv.book_update_view, name="update-book"),
    path('filter-books/', bv.filter_book, name='book-view'),
    path('filter-books/wishlist/', bv.wish_list, name='wish-list')
]
