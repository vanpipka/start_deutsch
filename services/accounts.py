from urllib.request import Request

from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseServerError, JsonResponse
from django.middleware import csrf

from myproject.models import AdditionalField

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.contrib.auth import login as auth_login, authenticate
from django.http import HttpResponseRedirect
from settings.constants import PSW_SALT


def profile(request: Request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login/")

    user_data = AdditionalField.get_by_id(request.user)

    if not user_data:
        return HttpResponseServerError("No user data")

    if request.method == 'POST':
        data = {
                "user": request.user,
                "email": request.POST["email"],
                "name": request.POST["name"],
                "phone": request.POST["phone"]
        }
        save_result = user_data.save_account(data)
        if save_result["error"]:
            return HttpResponseServerError(save_result.error_message)
        return render(request, 'accounts/profile.html', context={"user": user_data})
    else:
        return render(request, 'accounts/profile.html', context={"user": user_data})


def login(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/profile/")

    if request.method == 'POST':

        its_new_user = False

        form_copy = request.POST.copy()
        username = form_copy.get("username", "")
        username = username.replace("+", "").replace("(", "").replace(")", "").replace(" ", "")

        password = form_copy.get("password", "") + PSW_SALT

        form_copy['username'] = username
        form_copy['password'] = password
        form_copy['password1'] = password
        form_copy['password2'] = password

        if User.objects.filter(username=username).exists():
            its_new_user = True
            form = AuthenticationForm(request, data=form_copy)
        else:
            form = UserCreationForm(form_copy)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            form.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # логинимся
                    auth_login(request, user)
                    return JsonResponse({"result": True, 'csrfmiddlewaretoken': csrf.get_token(request)})
                else:
                    JsonResponse({"result": False, "error": "user desabled"})
            else:
                return JsonResponse({"result": False, "error": "user desabled"})

        elif not its_new_user:

            form_copy['email'] = username + "@xxx.com"  # для того чтобы использовать стандартные формы
            form = PasswordResetForm(form_copy)
            if form.is_valid():
                u = User.objects.get(username=username)
                u.set_password(password)
                u.save()

                user = authenticate(username=username, password=password)

                if user is not None:
                    if user.is_active:
                        # логинимся
                        auth_login(request, user)
                        return JsonResponse({"result": True, 'csrfmiddlewaretoken': csrf.get_token(request)})
                    else:
                        JsonResponse({"result": False, "error": "user desabled"})
                else:
                    return JsonResponse({"result": False, "error": "user desabled"})

        else:

            error_str = ""
            for key, value in form.errors.as_data().items():
                error_str += str(key) + ":" + str(value[0].message)
            return JsonResponse({"result": False, "errors": error_str})

    else:

        return render(request, 'accounts/login.html', context={})

