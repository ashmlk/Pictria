from django.conf.urls import url
from django.urls import path, include
from pictures import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("tags/<slug:tag>/", views.image_tags, name="image-tags"),
    path("latest/", views.latest, name="latest"),
    path("views/", views.top_viewed, name="most-viewed"),
    path("bookmarks/", views.bookmarks, name="bookmarks"),
    path("i/<str:hashed_id>/like/", views.like_image, name="like-image"),
    path("i/<str:hashed_id>/bookmark/", views.bookmark_image, name="bookmark-image"),
    path("i/<str:hashed_id>/edit/", views.edit_image, name="edit-image"),
    path("i/<str:hashed_id>/delete/", views.delete_image, name="image-delete"),
    path("create/", views.create_image, name="create-image"),
    path("create/collection/", views.create_image_collection, name="create-collection"),
    path("i/<str:hashed_id>/", views.view_image, name="view-image"),
    path("search", views.search, name="search"),
    path("results", views.results, name="results"),
    path("profile/settings/", views.settings, name="settings"),
    path(
        "profile/settings/personal-information/",
        views.edit_profile,
        name="settings-personal",
    ),
    path("profile/settings/privacy/", views.privacy, name="settings-privacy"),
    path("<str:username>/", views.view_profile_images, name="view-profile"),
    path(
        "<str:username>/collections/",
        views.view_profile_collections,
        name="view-profile-collections",
    ),
    path("", views.home, name="home"),
]
