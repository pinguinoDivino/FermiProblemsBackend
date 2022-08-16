import locale
from rest_framework import serializers
from problems.models import Problem, UserAnswer

locale.setlocale(locale.LC_ALL, 'en_US.utf8')


class UserAnswerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    problem = serializers.StringRelatedField(read_only=True)
    date = serializers.DateTimeField(read_only=True, format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = UserAnswer
        fields = '__all__'

    def create(self, validated_data):
        problem = Problem.objects.get(pk=validated_data.pop('problem_id'))
        user_answer = UserAnswer.objects.create(problem=problem, **validated_data)
        user_answer.save()
        return user_answer


class ProblemSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    added_at = serializers.DateField(read_only=True)
    is_valid = serializers.BooleanField(read_only=True)
    level = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Problem
        fields = "__all__"

    def get_added_at(self, instance):
        return instance.added_at.strftime('%d %B %Y')

    def get_level(self, instance):
        return instance.get_level()
