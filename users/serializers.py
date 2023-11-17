from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        # this tells the view that the we can "post" the password but not "get" it
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 8, "required": False}
        }

    # this is used by the create api view to create new users
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # styles are set for the browsable api and are optional
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    # override the function that validates the input to also generate a token
    # the validate function is run during the "post" request
    def validate(self, attrs):
        # first validate the fields
        super().validate(attrs)

        # token generation
        email = attrs.get("email")
        password = attrs.get("password")

        # we use email as username since we're using custom user model
        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )

        # is credentials are invalid
        if not user:
            msg = "Invalid Credentials"
            raise serializers.ValidationError(msg, code="authorization")

        # the ObtainAuthToken View needs the authenticated user
        # but since we use a custom user model
        # we need to authenticate and reassign
        attrs["user"] = user
        return attrs
