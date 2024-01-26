from django.shortcuts import render


def template_login(request):
    context = {}

    return render(request, "chat.html", context=context)
