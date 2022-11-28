from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model

User = get_user_model()


class UserListView(ListView):
    model = User

    template_name = "user_list.html"


class UserDetailView(DetailView):

    model = User
    template_name = "user_detail.html"
    context_object_name = "user"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related(
            "memberships",
            "memberships__roles",
            "memberships__roles__attachments",
            "memberships__roles__attachments__policy",
        )
        return qs
