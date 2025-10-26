import os

from dotenv import load_dotenv
from rest_framework import serializers

from users.models import Payment, User

load_dotenv()
MOD_GROUP = os.getenv("MOD_GROUP")


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "phone", "city", "avatar", "id")


class PaymentCheckoutSerializer(serializers.Serializer):
    payment_id = serializers.PrimaryKeyRelatedField(
        queryset=Payment.objects.all(), source="payment", write_only=True
    )

    checkout_url = serializers.URLField(read_only=True)
    session_id = serializers.CharField(read_only=True)

    def validate(self, attrs):
        payment = attrs["payment"]

        if not payment.amount or (payment.amount <= 0):
            raise serializers.ValidationError(
                "Сумма платежа должна быть положительной."
            )
        if not (payment.paid_course or payment.paid_lesson):
            raise serializers.ValidationError(
                "Платёж должен быть привязан к курсу или уроку."
            )
        return attrs
