import json
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from control import models
from datetime import date
from django.core import serializers
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def date_choice(request):
    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    request_date = json.loads(request.body)['date']
    parsed_date = date.fromisoformat(request_date)
    try:
        menus = models.MenuStructure.objects.filter(menu__week_day=weekdays[parsed_date.weekday()])
        response = get_products_from_menu(menus)
    except models.MenuStructure.DoesNotExist:
        return HttpResponse(json.dumps({'errors': [{'date': 'Меню на данный день не было составлено'}]}))
    return HttpResponse(json.dumps(response))


def get_products_data(menus):
    data = []
    for menu in menus:
        data.append(serializers.serialize('json', menu.products.all(), fields=('name',)))
    return data


def get_products_from_menu(menus):
    response = []
    for menu in menus:
        products = menu.products.all()
        menu_for_mealtime_type = []
        for product in products:
            menu_for_mealtime_type.append({'id': product.pk, 'name': product.name})
        response.append(menu_for_mealtime_type)
    return response


@csrf_exempt
def mealpoint(request, id):
    # command to test: curl -d "" http://127.0.0.1:8000/api/meal_point/military/<int: id>
    # its need to order exist for military with `id` for today

    channel_layer = get_channel_layer()
    today_order = models.Order.objects.filter(military_id=id).filter(date=date.today())
    if today_order:
        today_order = today_order[0]
        # order_item = models.OrderItem.objects.filter(order=today_order).filter(menu_structure__start_time__gte=x).filter(menu_structure__end_time__lte=x)
        order_items = models.OrderItem.objects.filter(order=today_order)
        if order_items:
            products = []
            for order_item in order_items:
                order_products = []
                for product in order_item.products.all():
                    order_products.append(product.name)
                products.append(order_products)
            print("api exec start")
            async_to_sync(channel_layer.group_send)("mealpoint", {
                "type": "mealpoint_message",
                "data": {
                    'military': {
                        'name': today_order.military_id.name,
                        'image': today_order.military_id.image.name,
                    },
                    # 'products': serializers.serialize('json', order_item.products.all(), fields=('name',))
                    'products': products
                },
            })
            print("api exec end")
            return HttpResponse('OK')
    # if order not register for today or unknown user
    return HttpResponseServerError()
