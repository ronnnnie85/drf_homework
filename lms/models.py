from django.db import models

from config import settings


class Course(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Укажите описание курса",
    )
    preview = models.ImageField(
        upload_to="lms/courses/avatars",
        blank=True,
        null=True,
        verbose_name="Превью курса",
        help_text="Укажите превью курса",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    name = models.CharField(
        max_length=150,
        verbose_name="Название урока",
        help_text="Укажите название урока",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание урока",
        help_text="Укажите описание урока",
    )
    preview = models.ImageField(
        upload_to="lms/lessons/avatars",
        blank=True,
        null=True,
        verbose_name="Превью урока",
        help_text="Укажите превью урока",
    )
    video = models.CharField(
        max_length=300,
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
