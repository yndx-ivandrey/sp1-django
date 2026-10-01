# mypy: ignore-errors
import json
import random
import re
import unicodedata
from datetime import timedelta
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Case, When
from django.utils import timezone
from faker import Faker

from blog.models import Comment, Post

fake = Faker("ru_RU")
User = get_user_model()

DATA_FILE = Path(__file__).parent / "posts_comments.json"
IMAGES_DIR = Path(__file__).parent / "img"
USERS_COUNT = 3
POSTS_PERIOD_DAYS = 90

TRANSLIT = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


def translit(value):
    prepared = unicodedata.normalize("NFKD", value.lower().replace("ё", "е"))
    result = "".join(TRANSLIT.get(char, char) for char in prepared)
    return re.sub(r"[^a-z0-9]+", "", result)


def random_between(start, end):
    seconds = (end - start).total_seconds()
    return start + timedelta(seconds=random.uniform(0, seconds))


def random_in_slots(start, end, count):
    """
    count неубывающих случайных дат в окне [start, end].

    Окно делится на count равных отрезков, в каждом берётся случайная точка,
    поэтому даты не сваливаются в конец окна, как при цепочке
    «от предыдущей даты до текущей».
    """
    if count <= 0:
        return []

    slot = (end - start) / count
    values = []

    for index in range(count):
        slot_start = start + index * slot
        values.append(random_between(slot_start, slot_start + slot))

    return values


class Command(BaseCommand):
    help = "Generate demo users, blog posts and comments"

    @transaction.atomic
    def handle(self, *args, **options):
        admin = User.objects.filter(username="admin").first()
        if admin is None:
            raise CommandError(
                'Пользователь "admin" не найден. Создайте его перед запуском команды.'
            )

        images = self.load_images()
        posts_data = self.load_posts()

        users = [admin, *self.create_users()]
        self.create_posts(users, posts_data, images)

    def create_users(self):
        users = []

        for _ in range(USERS_COUNT):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = self.make_username(translit(last_name))

            user = User.objects.create_user(
                username=username,
                email=f"{username}@test.test",
                password=None,
                first_name=first_name,
                last_name=last_name,
            )
            users.append(user)

            self.stdout.write(
                f"Создан пользователь: {username} ({user.email}), "
                f"{last_name} {first_name}"
            )

        return users

    def make_username(self, base):
        base = base or "user"
        username = base
        suffix = 1

        while User.objects.filter(username=username).exists():
            suffix += 1
            username = f"{base}{suffix}"

        return username

    def load_posts(self):
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            return data["posts"]
        except (OSError, ValueError, KeyError, TypeError) as error:
            raise CommandError(
                f"Не удалось прочитать данные из файла {DATA_FILE}: {error}"
            ) from error

    def load_images(self):
        if not IMAGES_DIR.is_dir():
            raise CommandError(f"Папка с изображениями не найдена: {IMAGES_DIR}")

        images = sorted(path for path in IMAGES_DIR.iterdir() if path.is_file())
        if not images:
            raise CommandError(f"В папке {IMAGES_DIR} нет ни одного изображения.")

        return images

    def create_posts(self, users, posts_data, images):
        now = timezone.now()
        published_dates = random_in_slots(
            now - timedelta(days=POSTS_PERIOD_DAYS), now, len(posts_data)
        )

        for number, (item, published_at) in enumerate(
            zip(posts_data, published_dates), start=1
        ):
            author = random.choice(users)
            image_path = random.choice(images)
            post = self.create_post(item, author, image_path, published_at)
            comments_count = self.create_comments(item, post, users, published_at, now)

            self.stdout.write(
                f"Пост {number}/{len(posts_data)}: "
                f"{published_at:%d.%m.%Y %H:%M} {post.title} "
                f"(автор: {author.username}, изображение: {post.image.name}, "
                f"комментариев: {comments_count})"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово: создано {USERS_COUNT} пользователя, "
                f"{len(posts_data)} постов и комментарии к ним."
            )
        )

    def create_post(self, item, author, image_path, published_at):
        # Файл из папки img копируется в MEDIA_ROOT при сохранении поста
        with image_path.open("rb") as image_file:
            post = Post.objects.create(
                title=item["title"],
                text=item["text"],
                author=author,
                image=File(image_file, name=image_path.name),
            )

        # auto_now_add перезаписывает дату при вставке, проставляем её отдельно
        Post.objects.filter(pk=post.pk).update(published_at=published_at)
        post.published_at = published_at

        return post

    def create_comments(self, item, post, users, published_at, now):
        texts = item.get("comments") or []
        if not texts:
            return 0

        possible_authors = [user for user in users if user.pk != post.author_id]

        comments = []
        created_at_values = []
        cursor = published_at

        for text in texts:
            created_at = random_between(cursor, now)
            cursor = created_at

            comments.append(
                Comment(
                    post=post,
                    author=random.choice(possible_authors),
                    text=text,
                )
            )
            created_at_values.append(created_at)

        Comment.objects.bulk_create(comments)
        self.set_comments_dates(post, created_at_values)

        return len(comments)

    def set_comments_dates(self, post, created_at_values):
        # auto_now_add перезаписывает даты при вставке, проставляем их отдельно
        ids = list(
            Comment.objects.filter(post=post)
            .order_by("id")
            .values_list("id", flat=True)
        )
        if len(ids) != len(created_at_values):
            raise CommandError(
                f"Не удалось сопоставить комментарии поста «{post.title}» с датами."
            )

        Comment.objects.filter(post=post).update(
            created_at=Case(
                *[
                    When(pk=pk, then=created_at)
                    for pk, created_at in zip(ids, created_at_values)
                ]
            )
        )
