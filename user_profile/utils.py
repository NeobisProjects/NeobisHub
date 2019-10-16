import random
import string


class Validate:
    @staticmethod
    def create_validation_code():
        validation_code = ''.join(random.choice(string.digits) for _ in range(6))
        return validation_code
