from myproject.models import Subscriber


def make_subscriber(request) -> bool:

    if request.method != 'POST':
        return False

    email: str = request.POST.get('email', '')

    if str(email) == '':
        return False

    if len(Subscriber.objects.all().filter(email=email)) != 0:
        return True

    subscriber = Subscriber()
    subscriber.email = email
    subscriber.save()

    return True

