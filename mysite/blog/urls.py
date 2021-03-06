from django.urls import path
from . import views

app_name = "blog"  # refer to the urls of the app inside app
urlpatterns = [
    # post views
    path("", views.PostListView.as_view(), name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),
    path("<int:post_id>", views.post_share, name="post_share"),
]
