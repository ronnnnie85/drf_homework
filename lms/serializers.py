import os

from dotenv import load_dotenv
from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import VideoURLValidator

load_dotenv()
MOD_GROUP = os.getenv("MOD_GROUP")


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.CharField(validators=[VideoURLValidator()])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

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
            "is_subscribed",
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

    def get_is_subscribed(self, obj: Course) -> bool:
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False
        return Subscription.objects.filter(user=user, course=obj).exists()


class SubscriptionToggleSerializer(serializers.Serializer):
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        write_only=True
    )

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())