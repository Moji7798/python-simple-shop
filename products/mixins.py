from django.contrib.auth.mixins import UserPassesTestMixin


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        # redirect to login page for anonymous users, else show 403
        from django.contrib.auth.views import redirect_to_login

        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path())
        from django.http import HttpResponseForbidden

        return HttpResponseForbidden("You don't have permission to access this page.")
