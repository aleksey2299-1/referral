from rest_framework.throttling import AnonRateThrottle


class CodeRequestThrottle(AnonRateThrottle):
    """Регулятор для запроса кода подтверждения."""

    rate = "10/min"
