import os

from dotenv import load_dotenv
from rest_framework import serializers

from users.models import Payment, User

load_dotenv()
MOD_GROUP = os.getenv('MOD_GROUP')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "phone", "city", "avatar", "id")


