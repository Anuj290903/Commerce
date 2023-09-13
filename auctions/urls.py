from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("item/<str:ID>", views.item, name="item"),
    path("category/<str:name>", views.category, name="category"),
    path("categories", views.categories, name="categories"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create_cat", views.create_cat, name="create_cat"),
    path("add_bid/<str:ID>", views.add_bid, name="add_bid"),
    path("close/<str:ID>", views.close, name="close"),
    path("add_comment/<str:ID>", views.add_comment, name="add_comment"),
    path("profile", views.user_prof, name="user_prof"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_list/<str:ID>", views.add_list, name="add_list"),
    path("remove_list/<str:ID>", views.remove_list, name="remove_list"),
    path("closed_listings", views.cls_listing, name="cls_listings")
]
