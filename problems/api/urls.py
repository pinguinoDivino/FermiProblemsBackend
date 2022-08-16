from django.urls import include, path
from rest_framework.routers import DefaultRouter
from problems.api import views as ev

router = DefaultRouter()
router.register(r"problems", ev.ProblemViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("problems/<int:id>/answers/", ev.UserAnswerListApiView.as_view()),
    path("problems/<int:id>/answers/create/", ev.UserAnswerCreateApiView.as_view()),
]
