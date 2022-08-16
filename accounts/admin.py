import types
from django import forms
from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AdminPasswordChangeForm

User = get_user_model()


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        # Use the pretty 'filter_horizontal widget'.
        widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance


class CustomUserAdmin(BaseUserAdmin):

    change_password_form = AdminPasswordChangeForm

    list_display = ('username', 'email', 'first_name', 'last_name', 'gender', 'birth_date', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        ("User", {'fields': ('username', 'email', 'password')}),
        ('Anagrafica', {'fields': ('first_name', 'last_name', 'gender', 'birth_date')}),
        ('Attività', {'fields': ('date_joined', 'last_login', 'is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Informazioni aggiuntive', {'fields': ('dpc', )})
    )

    readonly_fields = ['date_joined', 'last_login']

    add_fieldsets = (
        ("User", {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', "last_name", 'gender', 'birth_date', 'password1', 'password2', 'is_staff'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username', 'email', 'date_joined')

    list_per_page = 50


class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    filter_horizontal = ['permissions']


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)


def has_permission(self, request):
    return request.user.is_active and (request.user.is_staff or request.user.groups.filter(name='Managers').exists())


class GroupAdminAuthenticationForm(AdminAuthenticationForm):
    def confirm_login_allowed(self, user):
        if user.groups.filter(name="Managers").exists():
            user.is_staff = True
        super().confirm_login_allowed(user)


admin.site.site_header = 'Pannello di Amministrazione'
admin.site.index_title = 'Amministrazione'
admin.site.login_form = GroupAdminAuthenticationForm
admin.site.has_permission = types.MethodType(has_permission, admin.site)
