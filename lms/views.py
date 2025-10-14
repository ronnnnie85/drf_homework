import os

from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.paginators import LmsPagination
from lms.permissions import ModeratorsNoCreateDelete, OwnerOnlyForNonModerators
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionToggleSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [
        IsAuthenticated,
        ModeratorsNoCreateDelete,
        OwnerOnlyForNonModerators,
    ]
    pagination_class = LmsPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonCreateView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        ModeratorsNoCreateDelete,
        OwnerOnlyForNonModerators,
    ]

    def get_queryset(self):
        user = self.request.user
        is_moderator = user.groups.filter(name=os.getenv("MOD_GROUP")).exists()
        return (
            Course.objects.all() if is_moderator else Course.objects.filter(owner=user)
        )

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        ModeratorsNoCreateDelete,
        OwnerOnlyForNonModerators,
    ]
    pagination_class = LmsPagination

    def get_queryset(self):
        user = self.request.user
        is_moderator = user.groups.filter(name=os.getenv("MOD_GROUP")).exists()
        return (
            Lesson.objects.all() if is_moderator else Lesson.objects.filter(owner=user)
        )


class LessonRetrieveView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        ModeratorsNoCreateDelete,
        OwnerOnlyForNonModerators,
    ]


class LessonUpdateView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        ModeratorsNoCreateDelete,
        OwnerOnlyForNonModerators,
    ]


class LessonDestroyView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        ModeratorsNoCreateDelete,
        OwnerOnlyForNonModerators,
    ]


class SubscriptionToggleAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SubscriptionToggleSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        course = serializer.validated_data["course"]

        qs = Subscription.objects.filter(user=user, course=course)

        if qs.exists():
            qs.delete()
            message = "Подписка удалена"
            subscribed = False
            http_status = status.HTTP_200_OK
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"
            subscribed = True
            http_status = status.HTTP_201_CREATED

        return Response({"message": message, "subscribed": subscribed}, status=http_status)