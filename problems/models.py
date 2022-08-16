from random import randint
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from problems.decorators import cached

User = get_user_model()

LEVEL_TRESHOLD = 4

LEVELS = {
    1.00: _("Complesso"),
    0.75: _("Avanzato"),
    0.45: _("Medio"),
    0.15: _("Base"),
}


class ProblemManager(models.Manager):

    @cached
    def get_count(self, hours=1):
        return self.aggregate(count=Count('id'))['count']

    def random(self):
        count = self.get_count()
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class Problem(models.Model):
    question = models.CharField(_('domanda'), max_length=3000)
    value = models.FloatField(_('valore'))
    answer = models.CharField(_('risposta'), max_length=3000)
    explanation = models.TextField(_('spiegazione'))
    added_at = models.DateField(_('data di creazione'), auto_now_add=True)
    q_image = models.ImageField(_('immagine domanda'), upload_to="q_imgs/%Y/%m/%d", blank=True, null=True)
    a_image = models.ImageField(_('immagine domanda'), upload_to="a_imgs/%Y/%m/%d", blank=True, null=True)
    e_image = models.ImageField(_('immagine domanda'), upload_to="e_imgs/%Y/%m/%d", blank=True, null=True)

    author = models.ForeignKey(
        User,
        related_name='created_problems',
        verbose_name=_('autore'),
        on_delete=models.CASCADE
    )
    is_valid = models.BooleanField(_('è valida'), default=False)

    objects = ProblemManager()

    class Meta:
        db_table = 'problems'
        verbose_name = 'Problema'
        verbose_name_plural = 'Problemi'

    def __str__(self):
        if len(str(self.question)) > 1000:
            return self.question[:1000]
        return self.question

    @property
    def has_explanation(self):
        return bool(self.explanation)

    def get_distribution(self):
        pass

    def get_average_distance(self):
        dist_sum = 0
        for answer in UserAnswer.objects.filter(problem=self):
            dist_sum += answer.get_normalized_distance()

        return dist_sum / UserAnswer.objects.filter(problem=self).count()

    def get_approx_distance(self):
        return min(LEVELS.keys(), key=lambda x: abs(x - self.get_average_distance()))

    def get_level(self):
        if self.users_answers.count() > LEVEL_TRESHOLD:
            return LEVELS[self.get_approx_distance()]
        return LEVELS[sorted(LEVELS.keys(), key=lambda x: float(x))[1]]


class UserAnswer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name=_("utente")
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="users_answers",
        verbose_name=_("problema")
    )

    value = models.FloatField(_('valore'))
    date = models.DateTimeField(_('data'), auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = 'users_answers'
        verbose_name = 'Risposta utente'
        verbose_name_plural = 'Risposte utenti'

    def __str__(self):
        return "Risposta di {} al problema n. {}".format(self.user, self.problem.id)

    def get_normalized_distance(self):
        return abs((self.value - self.problem.value) / self.problem.value)
