from django import forms
from django.core import validators

from .models import Comment, Post


class PostForm(forms.ModelForm):  # type: ignore[type-arg]
    title = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Укажите название поста"}),
        label="Название поста",
        validators=[validators.MinLengthValidator(5)],
        error_messages={"required": "Название поста - обязательно"},
        strip=True,
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Укажите текст сообщения"}),
        label="Текст сообщения",
        validators=[validators.MinLengthValidator(10)],
        error_messages={"required": "Текст сообщения - обязателен"},
        strip=True,
    )

    image = forms.ImageField(required=False, label="Файл изображения")

    class Meta:
        model = Post
        fields = ("title", "text", "image")


class CommentForm(forms.ModelForm):  # type: ignore[type-arg]
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Укажите текст комментария", "rows": 4}
        ),
        label="Комментарий",
        validators=[validators.MinLengthValidator(10)],
        error_messages={"required": "Текст комментария - обязателен"},
        strip=True,
    )

    class Meta:
        model = Comment
        fields = ("text",)
        help_texts = {"text": "Оставьте Ваш комментарий"}  # noqa: RUF012
