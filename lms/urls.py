from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonCreateView, LessonListView, LessonRetrieveView, LessonUpdateView, LessonDestroyView

app_name = LmsConfig.name

router = SimpleRouter()
router.register(r'courses', CourseViewSet, basename='course')


urlpatterns = [
    path('lessons/', LessonListView.as_view(), name='lesson_list'),
    path('lessons/create/', LessonCreateView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/', LessonRetrieveView.as_view(), name='lesson'),
    path('lessons/<int:pk>/update/', LessonUpdateView.as_view(), name='lesson_update'),
    path('lessons/<int:pk>/delete/', LessonDestroyView.as_view(), name='lesson_destroy'),
]

urlpatterns += router.urls