"""snippets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drm.html_views import UserDetailView, UserListView
from drm.views import LicensesViewSet, OrganizationsViewSet, UsersViewSet

# from snippets.views import UserViewSet

router = routers.DefaultRouter()
# router.register(r"users", UserViewSet)
router.register(r"organizations", OrganizationsViewSet)
router.register(r"licenses", LicensesViewSet)
router.register(r"users", UsersViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/user/<str:pk>", UsersViewSet.as_view({"get": "list"}), name="user-detail"),
    path("users/", UserListView.as_view()),
    path("users/<str:pk>", UserDetailView.as_view()),
]
