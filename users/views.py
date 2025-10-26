from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings
from users import services
from users.models import Payment, User
from users.serializers import (
    PaymentSerializer,
    UserSerializer,
    PaymentCheckoutSerializer,
)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["paid_course", "paid_lesson", "payment_method"]
    ordering_fields = ["payment_date"]
    permission_classes = [IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserCreateApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentCheckoutCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PaymentCheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.validated_data["payment"]

        product_name = ""
        product_desc = ""

        if payment.paid_course:
            product_name = payment.paid_course.name
            product_desc = payment.paid_course.description
        elif payment.paid_lesson:
            product_name = payment.paid_lesson.name
            product_desc = payment.paid_lesson.description

        # 1) Product
        product = services.create_product(
            name=product_name,
            description=product_desc,
        )
        payment.stripe_product_id = product["id"]

        # 2) Price (сумма в копейках!)
        unit_amount = int(payment.amount) * 100
        price = services.create_price(
            product_id=payment.stripe_product_id,
            unit_amount=unit_amount,
            currency=getattr(settings, "STRIPE_CURRENCY"),
        )
        payment.stripe_price_id = price["id"]

        # 3) Checkout Session
        session = services.create_checkout_session(
            price_id=payment.stripe_price_id,
            success_url=getattr(settings, "STRIPE_SUCCESS_URL"),
            cancel_url=getattr(settings, "STRIPE_CANCEL_URL"),
        )
        payment.stripe_session_id = session["id"]
        payment.checkout_url = session["url"]
        payment.save(
            update_fields=[
                "stripe_product_id",
                "stripe_price_id",
                "stripe_session_id",
                "checkout_url",
                "status",
            ]
        )

        return Response(
            {
                "checkout_url": payment.checkout_url,
                "session_id": payment.stripe_session_id,
            },
            status=status.HTTP_201_CREATED,
        )
