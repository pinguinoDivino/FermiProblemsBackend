import locale
from rest_framework import serializers
from problems.models import Problem, UserAnswer, ProblemValidationByUser
from drf_extra_fields.fields import Base64ImageField

locale.setlocale(locale.LC_ALL, 'en_US.utf8')


class UserAnswerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    problem = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = UserAnswer
        fields = '__all__'

    def create(self, validated_data):
        problem = Problem.objects.get(pk=validated_data.pop('problem_id'))
        return UserAnswer.objects.create(problem=problem, **validated_data)


class ProblemSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateField(read_only=True, format="%d-%m-%Y")
    rejected_at = serializers.DateField(read_only=True, format="%d-%m-%Y")
    status = serializers.CharField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    dislikes = serializers.SerializerMethodField(read_only=True)
    level = serializers.SerializerMethodField(read_only=True)
    q_image = Base64ImageField(required=False)
    e_image = Base64ImageField(required=False)

    class Meta:
        model = Problem
        fields = "__all__"

    def get_likes(self, instance):
        if instance.is_pending:
            return instance.get_like_validation_count()
        return None

    def get_dislikes(self, instance):
        if instance.is_pending:
            return instance.get_dislike_validation_count()
        return None


class ProblemValidationByUserSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    problem = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = ProblemValidationByUser
        fields = "__all__"

    def create(self, validated_data):
        problem = Problem.objects.get(pk=validated_data.pop('problem_id'))
        return ProblemValidationByUser.objects.create(problem=problem, **validated_data)

