import os
from datetime import datetime, timedelta
import random
from rest_framework import viewsets, generics, views, status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser, MultiPartParser
from django.db.models import Q
from django.conf import settings
from rest_framework.response import Response
from problems.models import Problem, ProblemValidationByUser
from problems.choices import RATING_CHOICES
from problems.api.serializers import ProblemSerializer, ProblemValidationByUserSerializer
from problems.api.pagination import StandardResultsSetPagination
from problems.api.permissions import IsAuthorOrReadOnly, IsAuthorOrNotAllowed
from problems.services.utils import create_problem_user_answer_distribution, recursive_glob, \
    get_problem_distribution_graph_base64

PROBLEM_DISTRIBUTION_GRAPH_EXPIRY_AFTER = 7  # days


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all().order_by('created_at')
    serializer_class = ProblemSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
    pagination_class = StandardResultsSetPagination
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [IsAuthorOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(status="pending")


class UserProblemListAPIView(generics.ListAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)


class InValidationProblemRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Problem.objects.filter(status="pending")
    serializer_class = ProblemSerializer

    def get_queryset(self):
        ids = ProblemValidationByUser.objects.filter(user=self.request.user).values_list('problem__id',
                                                                                         flat=True).order_by('id')
        return self.queryset.exclude(Q(author=self.request.user) | Q(id__in=ids))

    def get_object(self):
        return self.get_queryset().first()


class ProblemValidationByUserCreateAPIView(generics.CreateAPIView):
    queryset = ProblemValidationByUser.objects.all()
    serializer_class = ProblemValidationByUserSerializer

    def perform_create(self, serializer):
        serializer.save(problem_id=self.kwargs.get('id'), user=self.request.user)


class ProblemValidationByUserListAPIView(generics.ListAPIView):
    queryset = ProblemValidationByUser.objects.all()
    serializer_class = ProblemValidationByUserSerializer
    permission_classes = [IsAuthorOrNotAllowed, ]

    def get_queryset(self):
        return self.queryset.filter(problem__id=self.kwargs.get('id'))


class ProblemValidationRatingChoicesAPIView(views.APIView):

    def get(self, request, format=None):
        my_choices = []
        choice_dict = dict(RATING_CHOICES)
        for key, value in choice_dict.items():
            item = {"label": value, "value": key}
            my_choices.append(item)
        return Response(my_choices, status=status.HTTP_200_OK)


class ProblemUserAnswerDistributionAPIView(views.APIView):
    queryset = Problem.objects.filter(status="accepted")
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        queryset = self.queryset
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, format=None, *args, **kwargs):
        problem = self.get_object()
        date = datetime.today().strftime("%d-%m-%Y")
        image_folder_path = settings.MEDIA_ROOT + "/problem_distributions"
        image_path = image_folder_path + "/problem_{}_distribution_{}.png".format(problem.id, date)

        existing_files = recursive_glob(image_folder_path, "problem_{}_distribution".format(problem.id))
        if len(existing_files) == 0 or \
                datetime.strptime(existing_files[0][1].split("_")[-1].replace(".png", ""), "%d-%m-%Y")+ \
                timedelta(days=PROBLEM_DISTRIBUTION_GRAPH_EXPIRY_AFTER) < datetime.today():
            if len(existing_files) > 0:
                os.remove(existing_files[0][0])
            elif problem.get_answer_count() < 100:
                return Response({"detail": "Need at least 100 answers to"}, status=status.HTTP_404_NOT_FOUND)
            data = problem.get_distribution()
            create_problem_user_answer_distribution(data, image_path)

        else:
            image_path = image_folder_path + "/" + existing_files[0][1]

        graph = get_problem_distribution_graph_base64(image_path)

        return Response(graph, status=status.HTTP_200_OK)

