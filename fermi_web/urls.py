"""fermi_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings

from core.views import IndexTemplateView

urlpatterns = [
    path('amministrazione/pannello/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path("api-auth/", include("rest_framework.urls")),
    path('api/', include('accounts.api.urls')),
    path('api/', include('problems.api.urls')),
    path('api/', include('games.api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns.append(
    re_path(r"^.*$", IndexTemplateView.as_view(), name="entry-point")
)
