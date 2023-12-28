from rest_framework.serializers import ModelSerializer
from base.models import *


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class ExpenseSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        # Hash the password before creating the user
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Hash the password before updating the user
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        return super().update(instance, validated_data)

class PaymentInformationSerializer(ModelSerializer):
    class Meta:
        model = PaymentInformation
        fields = '__all__'
