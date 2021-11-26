from rest_framework import serializers
from django.contrib.auth import authenticate
from movies.models import Movie, Genre, UserProfile
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Movie
        fields = '__all__'


class RegisterUserSerializer(serializers.Serializer):
    """
    User Details serializer to accept and validate register form data from User.
    """

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, max_length=30)
    password = serializers.CharField(required=True, max_length=100)

    def validate_password(self, password):
        """
            Validation for password
        :param password: string
        :return: error / string
        """
        if "password" not in self.initial_data or self.initial_data["password"] is None:
            raise serializers.ValidationError("Password cannot be empty")

        new_password = self.initial_data["password"]

        # password length should be greater than 12 char
        if len(new_password) < 12:
            raise serializers.ValidationError('Password must be 12 characters long')

        # password should atleast follow 3 out of the following 4 checks
        password_strength = [
            any(pass_char.isupper() for pass_char in new_password),  # uppercase char
            any(pass_char.islower() for pass_char in new_password),  # lowercase char
            any(pass_char.isdigit() for pass_char in new_password),  # digit char
            any(not pass_char.isalnum() for pass_char in new_password),  # special char
        ]

        if sum(password_strength) < 3:
            raise serializers.ValidationError("New password should meet at least three conditions out of four listed - ")

        return password

    def validate_email(self, attrs):
        email = self.initial_data.get("email")
        users = User.objects.filter(email=email)
        if users.exists():
            raise serializers.ValidationError("User with this email already exists")
        return email

    def validate_username(self, attrs):
        username = self.initial_data.get("username")
        users = User.objects.filter(username=username)
        if users.exists():
            raise serializers.ValidationError("This username is already taken, please try using a different one.")
        return username

    def create(self, validated_data):
        email = validated_data.pop("email")
        username = validated_data.pop("username")
        password = validated_data.pop("password")
        user = User.objects.create_user(username, email, password)
        userprofile, created = UserProfile.objects.get_or_create(user=user)
        return user


class LoginUserSerializer(serializers.Serializer):
    """

    """
    username = serializers.CharField(required=True, max_length=30)
    password = serializers.CharField(required=True, max_length=100)
    validation_messages = "Please enter a correct username and password. Note that both " "fields may be case-sensitive."

    def validate(self, data):
        request = self.context.get("request")
        username = request.data.get("username")
        password = request.data.get("password")

        if username and password:
            user = authenticate(request=request, username=username, password=password)
            # import ipdb;ipdb.set_trace()
            if not user:
                if User.objects.filter(email=username).exists():
                    try:
                        usr_obj = User.objects.get(username=username)
                        if not usr_obj.is_active:
                            raise serializers.ValidationError(self.validation_messages)
                    except User.DoesNotExist:
                        raise serializers.ValidationError(
                            "Incorrect username. Please make sure you are entering the Username you registered with."
                        )
                    raise serializers.ValidationError(self.validation_messages)
                raise serializers.ValidationError(self.validation_messages)
        else:
            raise serializers.ValidationError(self.validation_messages)

        data["user"] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = UserProfile
        fields = '__all__'
