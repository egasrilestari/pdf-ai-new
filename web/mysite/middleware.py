from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_urls = [
            reverse("login"),
            reverse("logout"),
        ]

        path = request.path_info

        # Cek session yang kamu simpan sendiri, misal 'user_name'
        if not request.session.get("user_name"):
            if not any(path.startswith(url) for url in exempt_urls):
                return redirect("login")

        response = self.get_response(request)
        return response
