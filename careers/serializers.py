from rest_framework import serializers
from .models import Career, Step, Material, Progress, Category, Subcategory, Topic, Page
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Page

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'order_num', 'content']

class TopicSerializer(serializers.ModelSerializer):
    pages = PageSerializer(many=True, read_only=True)  
    class Meta:
        model = Topic
        fields = ['id', 'title', 'order_num', 'content', 'pages']

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'title', 'icon', 'description']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'icon', 'description']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'title', 'type', 'url', 'description','content']

class StepSerializer(serializers.ModelSerializer):
    materials = MaterialSerializer(many=True, read_only=True)
    topics = TopicSerializer(many=True, read_only=True)
    class Meta:
        model = Step
        fields = ['id', 'title', 'order_num', 'description', 'materials','topics']

class CareerSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Career
        fields = ['id', 'title', 'description', 'icon', 'category', 'steps']

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['id', 'step', 'completed']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user