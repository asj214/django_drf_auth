from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Customer


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        max_length=100,
        validators=[UniqueValidator(queryset=Customer.objects.all())]
    )
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Customer
        fields = ['email', 'name', 'password', 'token']

    def create(self, validated_data):
        return Customer.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('LOGIN_EMAIL_REQUIRED')
        if password is None:
            raise serializers.ValidationError('LOGIN_PASSWORD_REQUIRED')

        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            raise serializers.ValidationError('LOGIN_EMAIL_PASSWORD_WRONG')

        if customer is None:
            raise serializers.ValidationError('LOGIN_EMAIL_PASSWORD_WRONG')

        if not customer.check_password(password):
            raise serializers.ValidationError('LOGIN_EMAIL_PASSWORD_WRONG')

        if not customer.is_active:
            raise serializers.ValidationError('LOGIN_USER_DEACTIVATED')

        customer.last_login = timezone.now()
        customer.save()

        return {
            'email': customer.email,
            'name': customer.name,
            'token': customer.token
        }


class CustomerSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = Customer
        fields = (
            'id',
            'name',
            'email',
            'password',
            'is_active',
            'last_login',
            'created_at',
            'updated_at'
        )