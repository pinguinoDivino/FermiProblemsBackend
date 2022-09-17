import math
from datetime import timedelta, datetime
from random import randint
from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from django.urls import reverse
from problems.decorators import cached
from problems.choices import RATING_CHOICES,  PROBLEM_STATUS_CHOICES

User = get_user_model()

EXPIRY_TIME_AFTER_REJECTION = 7  # days

MIN_VALIDATIONS = 100

VALIDATION_THRESHOLD = 0.85



now = datetime.now()


class ProblemManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(Q(rejected_at__lt=now.date() + timedelta(days=EXPIRY_TIME_AFTER_REJECTION))
                                             | Q(rejected_at=None))

    @cached
    def get_accepted_count(self, hours=1):
        return self.filter(status="accepted").aggregate(count=Count('id'))['count']

    def random(self, status="accepted"):
        random_index = randint(0, self.get_accepted_count() - 1)
        return self.filter(status=status)[random_index]


class Problem(models.Model):
    question = models.CharField(_('question'), max_length=3000)
    value = models.FloatField(_('correct value'))
    answer = models.CharField(_('answer'), max_length=3000)
    explanation = models.TextField(_('explanation'))
    created_at = models.DateField(_('created at'), auto_now_add=True)
    q_image = models.ImageField(_('question image'), upload_to="q_imgs/%Y/%m/%d", blank=True, null=True)
    e_image = models.ImageField(_('explanation image'), upload_to="e_imgs/%Y/%m/%d", blank=True, null=True)

    author = models.ForeignKey(
        User,
        related_name='created_problems',
        verbose_name=_('author'),
        on_delete=models.CASCADE
    )
    status = models.CharField(_('status'), choices=PROBLEM_STATUS_CHOICES, default="pending", max_length=10)

    rejected_at = models.DateField(_("rejected at"), blank=True, null=True, default=None)

    objects = ProblemManager()

    class Meta:
        db_table = 'problems'
        verbose_name = 'Problem'
        verbose_name_plural = 'Problems'

    def __str__(self):
        return self.question[:1000] if len(str(self.question)) > 1000 else self.question

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.pk,))

    #  validation and status

    @property
    def is_approved(self):
        return self.status == "approved"

    @property
    def is_pending(self):
        return self.status == "pending"

    def get_validation_count(self):
        return self.validations.count()

    def get_like_validation_count(self):
        return self.validations.filter(rating="like").count()

    def get_dislike_validation_count(self):
        return self.get_validation_count() - self.get_like_validation_count()

    def check_validation(self):
        if self.get_validation_count() > MIN_VALIDATIONS and \
                (self.get_like_validation_count() / self.get_validation_count()) > VALIDATION_THRESHOLD:
            self.status = "approved"
            self.save()

    # answers, distribution, level

    def get_answer_count(self):
        return self.users_answers.count()

    @staticmethod
    def get_answer_magnitude(number):
        return math.floor(math.log(number, 10))

    def get_distribution(self):
        return [self.get_answer_magnitude(x) for x in UserAnswer.objects.filter(problem=self).values_list('value', flat=True)]


class UserAnswer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name=_("user")
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="users_answers",
        verbose_name=_("problem")
    )

    value = models.FloatField(_('value'))
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = 'users_answers'
        verbose_name = 'User answer'
        verbose_name_plural = 'User answers'

    def __str__(self):
        return _("Answer of {} to problem n. {}".format(self.user, self.problem.id))


class ProblemValidationByUser(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, verbose_name=_("problem"),
                                related_name="validations")

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'), related_name="validations")

    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)

    rating = models.TextField(_("rating"), choices=RATING_CHOICES)

    comment = models.CharField(_("comment"), max_length=5000, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        db_table = 'problem_validations'
        verbose_name = 'Problems validation'
        verbose_name_plural = 'Problems validations'
        unique_together = ('problem', 'user')

    def __str__(self):
        return _("Validation by {} of problem n. {}".format(self.user, self.problem.id))
