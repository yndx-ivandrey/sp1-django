from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="blog_index"),
    # path('', views.IndexView.as_view(), name='blog_index'),
    path("new/", login_required(views.AddPost.as_view()), name="new_post"),
    path("<str:username>/", views.profile_view, name="profile"),
    path("<str:username>/<int:post_id>", views.post_view, name="post"),
]
