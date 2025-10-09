from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class LessonCreateView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonListView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonRetrieveView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonUpdateView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonDestroyView(DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
