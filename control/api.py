import json
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from control import models
from datetime import date, datetime
from django.core import serializers
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def date_choice(request):
    """
    Принимает на вход указанную дату. Возвращаюет список продуктов на конкретный день недели.
    """
    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    request_date = json.loads(request.body)['date']
    parsed_date = date.fromisoformat(request_date)
    try:
        menus = models.MenuStructure.objects.filter(menu__week_day=weekdays[parsed_date.weekday()])
        response = get_products_from_menu(menus)
    except models.MenuStructure.DoesNotExist:
        return HttpResponse(json.dumps({'errors': [{'date': 'Меню на данный день не было составлено'}]}))
    return HttpResponse(json.dumps(response))


def military_control_choice(request):
    """
    Возвращает список военнослужащих и информацию о статусе приема пищи.
    """
    request_date = json.loads(request.body)['date']
    military_control_data = []
    if request_date:
        parsed_date = date.fromisoformat(request_date)
        orders = models.Order.objects.filter(date=parsed_date).filter(
            military_id__company__name=request.user.username).order_by('military_id')
        order_items = models.OrderItem.objects.filter(order__in=orders).values('is_done')
        for order in orders:
            items = order_items.filter(order=order)
            military_control_data.append({
                'name': order.military_id.name,
                'breakfast': items[0]['is_done'],
                'lunch': items[1]['is_done'],
                'dinner': items[2]['is_done']
            })
    return HttpResponse(json.dumps(military_control_data))

def get_products_from_menu(menus):
    """
    Возвращает словарь с продуктами связанными с конкретным MealType
    """
    response = {
        'mealtime_types': [],
        'products': []
    }
    for menu in menus:
        response['mealtime_types'].append(menu.pk)
        products = menu.products.all()
        menu_for_mealtime_type = []
        for product in products:
            menu_for_mealtime_type.append({'id': product.pk, 'name': product.name})
        response['products'].append(menu_for_mealtime_type)
    return response


@csrf_exempt
def mealpoint(request, id):
    # command to test: `curl -d "" http://127.0.0.1:8000/api/meal_point/military/<int: id>`
    # order must exist for military with `id` for today
    channel_layer = get_channel_layer()
    today_order = models.Order.objects.filter(military_id=id).filter(date=date.today())
    now_time = datetime.now().time()
    if today_order:
        today_order = today_order[0]
        order_item = models.OrderItem.objects.filter(order=today_order) \
            .filter(menu_structure__start_time__lte=now_time) \
            .filter(menu_structure__end_time__gte=now_time)
        if order_item:
            async_to_sync(channel_layer.group_send)("mealpoint", {
                "type": "mealpoint_message",
                "data": {
                    'military': {
                        'name': today_order.military_id.name,
                        'image': today_order.military_id.image.name,
                    },
                    'products': order_item[0].get_products_list()
                },
            })
            order_item[0].check_as_done()
            return HttpResponse('OK')
    # if order not register for today or unknown user
    return HttpResponseServerError()
