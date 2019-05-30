
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.utils import timezone


def callback(request):
    return True


class DisableCFPMiddleware(MiddlewareMixin):
    def process_request(self, request):
        pass

    def process_response(self, request, response):
        """
        If request.session was modified, or if the configuration is to save the
        session every time, save the changes and set a session cookie or delete
        the session cookie if the session has been emptied.
        """
        difference = settings.DEADLINE_DATE - timezone.now()
        if "/proposals/submit/" in request.path and difference.days < 0:
            messages.error(request, "Proposal Submission deadline has passed!")
            response["Location"] = "/dashboard/"
            return redirect("dashboard")
        return response
