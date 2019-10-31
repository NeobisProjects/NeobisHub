import random
import string

from django.core.mail import EmailMultiAlternatives

from Hub.settings import EMAIL_HOST_USER


class Validate:
    @staticmethod
    def create_validation_code():
        validation_code = ''.join(random.choice(string.digits) for _ in range(4))
        return validation_code
# TODO: создать ф-ю отправки имейла красиво кодом валидации здесь и вызвать в сервисах

    @staticmethod
    def send_email_with_code(user):
        subject, from_email, to = 'Hub', EMAIL_HOST_USER, user.email
        text_content = ''
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.send()

    # def send_email_about_cheque(self, cheque: Cheque, products_data):
    #     subject, from_email, to = 'Магазин TECHmarket', EMAIL_HOST_USER, cheque.email
    #     text_content = ''
    #     cheque_list = ProductChequeList.objects.filter(cheque=cheque)
    #
    #     products = '\n'.join(
    #         ['{p}'.format(p=product.product.products)
    #          for product in cheque_list])
    #
    #     prices = '\n'.join(
    #         ['{w}'.format(w=product.product.price)
    #          for product in cheque_list])
    #     products_count = '\n'.join(
    #         ['{c}'.format(c=product.count)
    #          for product in cheque_list])
    #
    #     context = {'name': cheque.name,
    #                'id_cheque': cheque.id,
    #                'count': products_count,
    #                'total_sum': self.get_total_sum(cheque),
    #                'delivery': cheque.delivery_verbose(),
    #                'address': cheque.address,
    #                'product': products,
    #                'price': prices}
    #
    #     msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    #     msg.send()
