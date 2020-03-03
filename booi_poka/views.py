from allauth.account.forms import UserTokenForm
from allauth.account.views import PasswordResetFromKeyView as AllauthPasswordResetFromKeyView
from allauth.account.views import _ajax_response
from django.views.generic.edit import FormView


class PasswordResetFromKeyView(AllauthPasswordResetFromKeyView):

    def dispatch(self, request, uidb36, key, **kwargs):
        self.request = request
        self.key = key
        token_form = UserTokenForm(
            data={'uidb36': uidb36, 'key': self.key})
        if token_form.is_valid():
            # Store the key in the session and redirect to the
            # password reset form at a URL without the key. That
            # avoids the possibility of leaking the key in the
            # HTTP Referer header.
            # (Ab)using forms here to be able to handle errors in XHR #890
            token_form = UserTokenForm(
                data={'uidb36': uidb36, 'key': self.key})
            if token_form.is_valid():
                self.reset_user = token_form.reset_user
                return super(FormView, self).dispatch(request, uidb36, self.key, **kwargs)
        self.reset_user = None
        response = self.render_to_response(
            self.get_context_data(token_fail=True)
        )
        return _ajax_response(self.request, response, form=token_form)
