from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
                'username', 'password', 'role',
            )
        extra_kwargs = {
            'password' : {'write_only' : True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# class MemberOpsSerializezr(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = (
#             'username', 'password', 'first_name', 'last_name')
#         extra_kwargs = {
#             'password' : {'write_only' : True}
#         }

#     def update(self, instance, validated_data):
#         password = validated_data.pop('password')
#         instance = self.Meta.model(**validated_data)
#         instance.set_password(password)
#         instance.save()
#         return instance