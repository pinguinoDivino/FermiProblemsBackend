from django.contrib import admin
from problems.models import Problem, UserAnswer
# Register your models here.


class UserAnswerTabularInline(admin.TabularInline):
    model = UserAnswer


class ProblemAdmin(admin.ModelAdmin):

    inlines = (
        UserAnswerTabularInline,
    )

    list_display = ('question', 'value', 'added_at', 'author')


class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ("problem", 'value', 'user', 'date')


admin.site.register(Problem, ProblemAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)

