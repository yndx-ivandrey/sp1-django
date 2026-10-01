from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    text = models.TextField(verbose_name=_("Post Text"))
    author = models.ForeignKey(
        User,
        verbose_name=_("Author"),
        related_name="posts",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        verbose_name=_("Image"), upload_to="posts/%Y/%m", blank=True, null=True
    )
    published_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Publish Date"), db_index=True
    )

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ("-published_at",)

    def __str__(self) -> str:
        return f"{self.id} - {self.title}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Comment"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Author"),
    )
    text = models.TextField(verbose_name=_("Comment text"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"#{self.id}"
