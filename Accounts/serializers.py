from rest_framework import serializers
from .models import *

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

class InterestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interests
        fields = ["interest"]


#This is the UserModel stuff----------------------------------------------
class UserModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required = False)
    username = serializers.CharField(required = False)
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name","password" ]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        if not password:
            raise serializers.ValidationError("password is not provided")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop("password",None)
        if password:
            instance.set_password(password)
            
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        return instance

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()
    url = serializers.SerializerMethodField()
    interests = InterestModelSerializer(many=True, required = False, read_only=True)
    profile_picture = serializers.SerializerMethodField(required = False)
    class Meta:
        model = UserProfile
        fields = ["url","user","bio","profile_picture","website","DOB","banned","interests","facebook_link","twitter_link","instagram_link","linkedin_link"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        usermodel = UserModelSerializer.create(UserModelSerializer(),validated_data = user_data)
        usermodel.groups.add("User")
        interests_data = validated_data.pop("interests", None)
        if interests_data:
            for interest in interests_data:
                Interests.objects.create(User = usermodel, **interest)
        profile = UserProfile.objects.create(user = usermodel , **validated_data)
        profile.save()
        return profile
    
    def update(self, instance, validated_data):
        if user_data := validated_data.pop("user"):
            UserModelSerializer().update(instance=instance.user, validated_data=user_data)
        interests_data = validated_data.pop("interests", None)
        print(interests_data)
        if interests_data:
            print(interests_data)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance

    
    def get_url(self, obj):
        return f"http://127.0.0.1:8000/accounts/user/{obj.user.id}"
    
    def get_profile_picture(self, obj):
        try:
            return obj.profile_picture.profile_picture.url
        except:
            return None


#this is the adminmodel stuff---------------------------------------
class AdminProfileSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()
    url = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField(required = False)
    class Meta:
        model = AdminProfile
        fields = ["url","user","bio","profile_picture","phone_number","address"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        usermodel = UserModelSerializer.create(UserModelSerializer(),validated_data = user_data)
        usermodel.groups.add("Admin")
        profile = AdminProfile.objects.create(user = usermodel , **validated_data)
        profile.save()
        return profile
    
    def update(self, instance, validated_data):
        if user_data := validated_data.pop("user"):
            UserModelSerializer().update(instance=instance.user, validated_data=user_data)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance

    
    def get_url(self, obj):
        return f"http://127.0.0.1:8000/accounts/user/{obj.user.id}"
    
    def get_profile_picture(self, obj):
        try:
            if obj.profile_picture.exists():
              return obj.profile_picture.profile_picture.url  
            else:
                return None
        except:
            return "something went wrong while fetching profile picture"


#this is the mobmodel stuff---------------------------------------
class MobProfileSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()
    url = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField(required = False)
    class Meta:
        model = MobProfile
        fields = ["url","user","bio","profile_picture","phone_number","address","position","employment_date","emergency_contact","linkedin_profile"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        usermodel = UserModelSerializer.create(UserModelSerializer(),validated_data = user_data)
        if validated_data["position"].lower() == "super":
            usermodel.groups.clear()
            usermodel.groups.add("MobSuper")
        else:
            usermodel.groups.clear()
            usermodel.groups.add("MobBeta")
        profile = MobProfile.objects.create(user = usermodel , **validated_data)
        profile.save()
        return profile
    
    def update(self, instance, validated_data):
        if user_data := validated_data.pop("user"):
            UserModelSerializer().update(instance=instance.user, validated_data=user_data)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance

    
    def get_url(self, obj):
        return f"http://127.0.0.1:8000/accounts/user/{obj.user.id}"
    
    def get_profile_picture(self, obj):
        try:
            if obj.profile_picture.exists():
              return obj.profile_picture.profile_picture.url  
            else:
                return None
        except:
            return "something went wrong while fetching profile picture"
        