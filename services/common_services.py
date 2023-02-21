from datetime import timedelta
from django.utils import timezone


def check_if_new(date):
    min_date = timezone.now() - timedelta(days=7)
    return True if date > min_date else False


def check_object_exist(func):
    def wrapper(self, *args, **kwargs):
        if not self:
            return None
        return func(self, *args, **kwargs)
    return wrapper
