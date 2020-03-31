import random
import string

from django.core.mail import EmailMultiAlternatives

from Hub.settings import EMAIL_HOST_USER


class Validate:
    @staticmethod
    def create_validation_code():
        validation_code = ''.join(random.choice(string.digits) for _ in range(4))
        return validation_code

    @staticmethod
    def send_email_with_code(user, code):
        subject, from_email, to = 'Hub', EMAIL_HOST_USER, user.email
        text_content = f'Ваш код подтверждения: {code} '
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.send()

    @staticmethod
    def send_email_to_admin(user, surname, name):
        subject, from_email, to = 'Hub', EMAIL_HOST_USER, user.email
        text_content = '{surname}  {name} запрашиает статус HQ клуба Neobis.'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.send()
