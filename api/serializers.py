from rest_framework import serializers
from app.models import CustomUser
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from app.models import mobile_validate
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
    password = serializers.CharField(
  write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    mobile_no = serializers.CharField(max_length=10, validators=[mobile_validate])
    print("yes")
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "mobile_no","state","city","address","zipcode","password","password2" ]
            
        
    def validate(self, attrs):
        print("yes")
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs
    def create(self, validated_data):
        user = User.objects.create(
        email=validated_data['email'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],
        mobile_no = validated_data['mobile_no'],
        address =validated_data['address'],
        city = validated_data['city'],
        zipcode =validated_data['zipcode'],
        # state =validated_data['state'],
        )
       
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class ProfileUpdateSeializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["first_name", "last_name", "email", "mobile_no","state","city","address","zipcode" ]