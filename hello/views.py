from django.shortcuts import render

from django.shortcuts import redirect
from cases.views import index as case_index
from users.views import login as login_index


def index(request, user=None):
    if user:
        return redirect(case_index, user=user)

    return redirect(login_index)
