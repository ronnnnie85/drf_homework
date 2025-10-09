import os

from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from lms.permissions import ModeratorsNoCreateDelete, OwnerOnlyForNonModerators


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, ModeratorsNoCreateDelete, OwnerOnlyForNonModerators]

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonCreateView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ModeratorsNoCreateDelete, OwnerOnlyForNonModerators]

    def get_queryset(self):
        user = self.request.user
        is_moderator = user.groups.filter(name=os.getenv("MOD_GROUP")).exists()
        return Course.objects.all() if is_moderator else Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ModeratorsNoCreateDelete, OwnerOnlyForNonModerators]

    def get_queryset(self):
        user = self.request.user
        is_moderator = user.groups.filter(name=os.getenv("MOD_GROUP")).exists()
        return Lesson.objects.all() if is_moderator else Lesson.objects.filter(owner=user)


class LessonRetrieveView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ModeratorsNoCreateDelete, OwnerOnlyForNonModerators]


class LessonUpdateView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ModeratorsNoCreateDelete, OwnerOnlyForNonModerators]


class LessonDestroyView(DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ModeratorsNoCreateDelete, OwnerOnlyForNonModerators]
