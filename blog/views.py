from typing import Any

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView

from .forms import CommentForm, PostForm
from .models import Comment, Post

User = get_user_model()


@cache_page(20, key_prefix="index")
def index(request: HttpRequest) -> HttpResponse:
    posts = (
        Post.objects.select_related(
            "author",
        )
        .prefetch_related("comments")
        .all()
    )
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request, "blog/posts.html", {"page_obj": page_obj, "paginator": paginator}
    )


class IndexView(ListView):  # type: ignore[type-arg]
    """Пример Class Based View"""

    model = Post
    template_name = "blog/posts.html"
    paginate_by = 5
    context_object_name = "page"
    queryset = Post.objects.select_related("author").prefetch_related("comments").all()


class AddPost(View):
    form_class = PostForm
    template_name = "blog/new_post.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        post = Post()
        post.author = request.user  # type: ignore[assignment]
        form = self.form_class(
            request.POST or None, files=request.FILES or None, instance=post
        )
        if form.is_valid():
            post.save()
            return redirect("blog_index")
        return render(request, self.template_name, {"form": form})


def post_view(request: HttpRequest, username: str, post_id: int) -> HttpResponse:
    post = get_object_or_404(
        Post.objects.select_related("author").annotate(
            posts_amount=Count("author__posts")
        ),
        id=post_id,
        author__username=username,
    )
    comments = post.comments.select_related("author").all()
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(
                request, "Вы должны войти в систему, чтобы добавить комментарий."
            )
            return redirect("login")
        comment = Comment()
        comment.author = request.user
        comment.post = post
        comment_form = CommentForm(request.POST or None, instance=comment)
        if comment_form.is_valid():
            comment.save()
            messages.success(request, "Комментарий успешно добавлен!")
            return redirect(request.path_info)
    else:
        comment_form = CommentForm()
    return render(
        request,
        "blog/post.html",
        {
            "post": post,
            "author": post.author,
            "posts_amount": post.posts_amount,  # type: ignore[attr-defined]
            "form": comment_form,
            "comments": comments,
        },
    )


def profile_view(request: HttpRequest, username: str) -> HttpResponse:
    author = get_object_or_404(User, username=username)
    posts = author.posts.prefetch_related("comments").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request,
        "blog/profile.html",
        {
            "author": author,
            "posts_amount": paginator.count,
            "page": page,
            "paginator": paginator,
        },
    )
