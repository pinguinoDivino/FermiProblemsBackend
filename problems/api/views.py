from rest_framework import viewsets, generics, status
from rest_framework.response import Response
import json
from problems.api.pagination import StandardResultsSetPagination
from problems.models import Problem, UserAnswer
from problems.api.serializers import ProblemSerializer, UserAnswerSerializer
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all().order_by('added_at', )
    serializer_class = ProblemSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
    pagination_class = StandardResultsSetPagination
    parser_classes = [MultiPartParser, JSONParser]

    def create(self, request, *args, **kwargs):
        blob = request.data.pop("document")[0]
        data = json.loads(blob.read().decode()) | request.data.dict()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserAnswerListApiView(generics.ListAPIView):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

    def get_queryset(self):
        return self.queryset.filter(problem=Problem.objects.get(id=self.kwargs.get('id')))


class UserAnswerCreateApiView(generics.CreateAPIView):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

    def perform_create(self, serializer):
        serializer.save(problem_id=self.kwargs.get('id'), user=self.request.user)

        

