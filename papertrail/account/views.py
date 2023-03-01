from django.views.generic import TemplateView

from .utils import activate_user


class ActivateUserTemplateView(TemplateView):
    template_name = 'account/activate_user.html'

    def get(self, request, uid, token):
        activate_user(request, uid, token)
        return super().get(request)
