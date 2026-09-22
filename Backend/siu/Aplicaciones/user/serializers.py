from rest_framework import serializers
from Aplicaciones.user.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        update_user = super().update(instance, validated_data)
        update_user.set_password(validated_data['password'])
        update_user.save()
        return update_user
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = instance.id
        data['name'] = instance.name
        data['email'] = instance.email
        return data

"""
class TestUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("El correo electrónico no puede estar vacío.")
        return value
    
    def validate(self, data):
        return data
    
    def create(self, validated_data):
        return self.model.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
    
    class Meta:
        model = User
        fields = ['name', 'email']
"""