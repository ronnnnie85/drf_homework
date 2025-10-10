import os

from dotenv import load_dotenv
from rest_framework import serializers

from lms.models import Course, Lesson

load_dotenv()
MOD_GROUP = os.getenv("MOD_GROUP")


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "preview",
            "description",
            "lessons_count",
            "lessons",
            "owner",
        )

    def _filtered_lessons_qs(self, course: Course):
        request = self.context.get("request")
        if not request or not request.user or not request.user.is_authenticated:
            return Lesson.objects.none()

        user = request.user
        is_moderator = user.groups.filter(name=MOD_GROUP).exists()

        qs = course.lesson_set.all()
        if is_moderator:
            return qs
        return qs.filter(owner=user)

    def get_lessons(self, obj: Course):
        qs = self._filtered_lessons_qs(obj)

        return LessonSerializer(qs, many=True, context=self.context).data

    def get_lessons_count(self, obj: Course) -> int:
        return self._filtered_lessons_qs(obj).count()
