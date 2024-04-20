import random


def generate_confirmation_code() -> int:
    """Генерация кода подтверждения."""
    code = random.randrange(1000, 9999)
    return code
