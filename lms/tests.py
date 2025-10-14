from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson


class LessonTestCase(APITestCase):
    def setUp(self):
        # Создание пользователей
        self.user = get_user_model().objects.create_user(
            email="user@test.com", password="testpassword"
        )
        self.owner = get_user_model().objects.create_user(
            email="owner@test.com", password="testpassword"
        )

        # Создание курса
        self.course = Course.objects.create(
            name="Test Course", description="Test Course Description", owner=self.owner
        )

        # Создание уроков
        self.lesson_1 = Lesson.objects.create(
            course=self.course,
            name="Lesson 1",
            description="Content of lesson 1",
            owner=self.owner
        )

    def test_create_lesson(self):
        """Тест: создание урока"""
        self.client.force_authenticate(user=self.owner)
        data = {
            "course": self.course.id,
            "name": "New Lesson",
            "description": "New lesson content",
            "video": "https://youtube.com/watch?v=abc"
        }
        response = self.client.post("/lms/lessons/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_lesson(self):
        """Тест: обновление урока"""
        self.client.force_authenticate(user=self.owner)
        data = {
            "name": "Updated Lesson 1",
            "description": "Updated content of lesson 1",
            "video": "https://youtube.com/watch?v=abc"
        }
        response = self.client.put(f"/lms/lessons/{self.lesson_1.id}/update/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson_1.refresh_from_db()
        self.assertEqual(self.lesson_1.name, "Updated Lesson 1")

    def test_delete_lesson(self):
        """Тест: удаление урока"""
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(f"/lms/lessons/{self.lesson_1.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_read_lesson(self):
        """Тест: чтение урока"""
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(f"/lms/lessons/{self.lesson_1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.lesson_1.name)

    def test_unauthorized_user_create_lesson(self):
        """Тест: попытка создать урок без аутентификации"""
        data = {
            "course": self.course.id,
            "name": "Unauthorized Lesson",
            "description": "Unauthorized lesson content",
        }
        response = self.client.post("/lms/lessons/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_update_lesson(self):
        """Тест: попытка обновить урок без прав"""
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "Updated Unauthorized Lesson",
            "description": "Unauthorized content update",
        }
        response = self.client.put(f"/lms/lessons/{self.lesson_1.id}/update/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            email="owner@test.com", password="testpassword"
        )

        self.course = Course.objects.create(
            name="Test Course", description="Test Course Description", owner=self.owner
        )

    def test_subscribe_to_course(self):
        """Тест: подписка на курс"""
        self.client.force_authenticate(user=self.owner)
        data = {"course": self.course.id}
        response = self.client.post("/lms/subscription/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["subscribed"])

    def test_unsubscribe_from_course(self):
        """Тест: отписка от курса"""
        # Сначала подписываемся
        self.client.force_authenticate(user=self.owner)
        data = {"course": self.course.id}
        self.client.post("/lms/subscription/", data, format="json")

        # Теперь отписываемся
        response = self.client.post("/lms/subscription/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["subscribed"])

