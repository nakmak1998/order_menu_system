from django.shortcuts import render


def index(request):
    return render(request, 'control/index.html', {})


# TODO: сделать таблицу количества продуктов на закупку
# TODO: сделать таблицу выполненных заказов для роты на определенный день

