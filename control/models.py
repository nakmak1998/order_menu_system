from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.

class ProductType(models.Model):
    name = models.CharField("Тип блюда", max_length=200)

    class Meta:
        verbose_name = "тип блюда"
        verbose_name_plural = "Типы блюд"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("Название блюда", max_length=200)
    type = models.ForeignKey(ProductType, verbose_name="Тип блюда", on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name


class Menu(models.Model):
    WEEK_DAYS = [
        ('Понедельник', 'Понедельник'),
        ('Вторник', 'Вторник'),
        ('Среда', 'Среда'),
        ('Четверг', 'Четверг'),
        ('Пятница', 'Пятница'),
        ('Суббота', 'Суббота'),
        ('Воскресенье', 'Воскресенье'),
    ]
    week_day = models.CharField("День недели", choices=WEEK_DAYS, max_length=20)

    class Meta:
        verbose_name = "меню"
        verbose_name_plural = "Меню"

    def __str__(self):
        return self.week_day


class MenuStructure(models.Model):
    MEALTIME_TYPES = [
        ('Завтрак', 'Завтрак'),
        ('Обед', 'Обед'),
        ('Ужин', 'Ужин')
    ]
    menu = models.ForeignKey(Menu, verbose_name="Меню", on_delete=models.DO_NOTHING)
    mealtime_type = models.CharField("Тип приема пищи", choices=MEALTIME_TYPES, max_length=20)
    products = models.ManyToManyField(Product, verbose_name="Продукты")
    start_time = models.TimeField("Время начала приема пищи", default='13:00')
    end_time = models.TimeField("Время окончания приема пищи", default='15:00')

    def __str__(self):
        return f"{self.menu.week_day} {self.mealtime_type}"

    class Meta:
        verbose_name = "Структура меню"
        verbose_name_plural = "Структура меню"


class Company(models.Model):
    name = models.CharField("Название подразделения", max_length=200)

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"

    def __str__(self):
        return self.name


class Military(models.Model):
    RANKS = [
        ('ряд.', 'рядовой'),
        ('ефр.', 'ефрейтор'),
        ('мл. с-т.', 'младший сержант'),
        ('с-т.', 'сержант'),
        ('ст. с-т.', 'старший сержант'),
        ('пр-к.', 'прапорщик'),
        ('ст пр-к.', 'старший прапорщик'),
        ('мл. л-т.', 'младший лейтенант'),
        ('л-т.', 'лейтенант'),
        ('ст. л-т.', 'старший лейтенант'),
        ('к-н.', 'капитан'),
        ('м-р.', 'майор'),
        ('подп-к.', 'подполковник'),
        ('п-к.', 'полковник'),
    ]

    name = models.CharField("Имя", max_length=200)
    rank = models.CharField("Воинское звание", choices=RANKS, max_length=100)
    company = models.ForeignKey(Company, verbose_name="Название подразделения", on_delete=models.DO_NOTHING)
    image = models.ImageField("Фотография военнослужащего", upload_to='military/')

    def save(self, *args, **kwargs):
        self.image.name = f"{self.pk}.jpg"
        super(Military, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "военнослужащий"
        verbose_name_plural = "Военнослужащие"

    def __str__(self):
        return f'{self.rank} {self.name}'


class Order(models.Model):
    military_id = models.ForeignKey(Military, verbose_name="Военнослужащий", on_delete=models.DO_NOTHING)
    date = models.DateField("Дата приема пищи")

    def clean(self):
        qs_len = len(Order.objects.filter(date=self.date).filter(military_id=self.military_id))
        if qs_len > 1:
            raise ValidationError(
                'Невозможно создать заказ. Заказ на данный день на данного военнослужащего уже зарегистрирован'
            )
        return super(Order, self).clean()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'Заказ на {self.date} от {self.military_id}'


class OrderItem(models.Model):
    menu_structure = models.ForeignKey(MenuStructure, verbose_name="Тип приема пищи", on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, verbose_name="Заказ", on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, verbose_name="Блюда")
    is_done = models.BooleanField("Отметка о выполнении заказа", null=True)

    class Meta:
        verbose_name = "Заказ на прием пищи"
        verbose_name_plural = "Заказы на приемы пищи"

    def get_products_list(self):
        products = []
        for product in self.products.all():
            products.append(product.name)
        return products

    def get_products_num_by_type(self):
        x = self.products.all()
        print(x.values('name').annotate(models.Sum('name')))

    def check_as_done(self):
        self.is_done = True
        self.save()

    def __str__(self):
        return f"Заказ № {self.pk}"