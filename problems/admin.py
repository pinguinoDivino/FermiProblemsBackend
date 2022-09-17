from django.contrib import admin
from problems.models import Problem, UserAnswer, ProblemValidationByUser


class UserAnswerTabularInline(admin.TabularInline):
    model = UserAnswer


class ProblemAdmin(admin.ModelAdmin):
    inlines = (
        UserAnswerTabularInline,
    )

    list_display = ('id', '__str__', 'value', 'created_at', 'author', 'status')

    list_filter = ["status"]

    search_fields = ["question"]

    ordering = ["created_at"]


class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ("problem", 'value', 'user', 'created_at')

    search_fields = ["problem__question"]


class ProblemValidationByUserAdmin(admin.ModelAdmin):
    list_display = ("problem", "user", "created_at", "rating")

    search_fields = ["problem__question"]

    list_filter = ["rating"]

    ordering = ["created_at"]


admin.site.register(Problem, ProblemAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
admin.site.register(ProblemValidationByUser, ProblemValidationByUserAdmin)
