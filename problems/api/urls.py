from django.urls import include, path
from rest_framework.routers import DefaultRouter
from problems.api import views as ev

router = DefaultRouter()
router.register(r"problems", ev.ProblemViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("problems/user/list/", ev.UserProblemListAPIView.as_view()),
    path("problems/in-validation/first/", ev.InValidationProblemRetrieveAPIView.as_view()),
    path("problems/<int:id>/validation/create/", ev.ProblemValidationByUserCreateAPIView.as_view()),
    path("problems/<int:id>/validations/", ev.ProblemValidationByUserListAPIView.as_view()),
    path("problems/choices/ratings/", ev.ProblemValidationRatingChoicesAPIView.as_view()),
    path("problems/<int:id>/distribution/", ev.ProblemUserAnswerDistributionAPIView.as_view()),
]
