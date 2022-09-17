from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from problems.models import ProblemValidationByUser, Problem
from datetime import datetime
from problems.services.utils import file_cleanup


@receiver(post_save, sender=ProblemValidationByUser)
def update_problem_status(sender, instance, **kwargs):
    obj = instance.problem

    if instance.user.has_permission_to_validate_problems():
        obj.status = "accepted" if instance.rating == "like" else "rejected"
        obj.save()
    else:
        obj.check_validation()


@receiver(pre_save, sender=Problem)
def update_problem_rejected_date(sender, instance, **kwargs):

    if instance.pk is None:
        return

    old_status = Problem.objects.get(id=instance.id).status
    new_status = instance.status

    if old_status != "rejected" and new_status == "rejected":
        instance.rejected_at = datetime.now().date()

    elif old_status == "rejected" and new_status != "rejected":
        instance.rejected_at = None


@receiver(post_delete, sender=Problem)
def cleanup_problem_files(sender, instance, **kwargs):
    file_cleanup(sender=sender, instance=instance)
