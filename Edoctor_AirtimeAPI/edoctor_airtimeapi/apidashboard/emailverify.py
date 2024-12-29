from verify_email.email_handler import send_verification_email, _VerifyEmail
from django.template.loader import render_to_string
from django.core.mail import send_mail


class EdocVerify(_VerifyEmail):

    def __send_email(self, msg, useremail):
        return super()._VerifyEmail__send_email(msg, useremail)

    def send_email_verification(self, request, dashboard_user):
        user_to_verify = dashboard_user.user
        user_email = user_to_verify.email
        verification_url = self.token_manager.generate_link(
            request, user_to_verify, user_email)
        msg = render_to_string(
            self.settings.get('html_message_template', raise_exception=True),
            {"link": verification_url, "inactive_user": dashboard_user},
            request=request
        )
        self.__send_email(msg, user_email)

        return user_email
