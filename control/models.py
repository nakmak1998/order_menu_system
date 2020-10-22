from django.db import models


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
    type = models.ForeignKey(ProductType, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "Продукты"


    def __str__(self):
        return self.name


class MenuStructure(models.Model):
    WEEK_DAYS = [
        ('Понедельник', 'Понедельник'),
        ('Вторник', 'Вторник'),
        ('Среда', 'Среда'),
        ('Четверг', 'Четверг'),
        ('Пятница', 'Пятница'),
        ('Суббота', 'Суббота'),
        ('Воскресенье', 'Воскресенье'),
    ]

    MEALTIME_TYPES = [
        ('Завтрак', 'Завтрак'),
        ('Обед', 'Обед'),
        ('Ужин', 'Ужин')
    ]
    mealtime_type = models.CharField(choices=MEALTIME_TYPES, max_length=20)
    week_day = models.CharField(choices=WEEK_DAYS, max_length=20)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.week_day + " - " + self.mealtime_type

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
        ('ефр', 'ефрейтор'),
        ('мл. с-т', 'младший сержант'),
        ('с-т', 'сержант'),
        ('ст. с-т', 'старший сержант'),
        ('пр-к', 'прапорщик'),
        ('ст пр-к', 'старший прапорщик'),
        ('мл. л-т', 'младший лейтенант'),
        ('л-т', 'лейтенант'),
        ('ст. л-т', 'старший лейтенант'),
        ('к-н', 'капитан'),
        ('м-р', 'майор'),
        ('подп-к', 'подполковник'),
        ('п-к', 'полковник'),
    ]

    name = models.CharField("Имя", max_length=200)
    rank = models.CharField("Воинское звание", choices=RANKS, max_length=100)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "военнослужащий"
        verbose_name_plural = "Военнослужащие"

    def __str__(self):
        return self.rank + " " + self.name


class Order(models.Model):
    military_id = models.ForeignKey(Military, verbose_name="Военнослужащий", on_delete=models.DO_NOTHING)
    date = models.DateField("Дата приема пищи")
    products = models.ManyToManyField(Product)
    is_done = models.BooleanField("Статус заказа")

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ № {self.pk}"


#
# class Menu(models.Model):
#     date = models.DateField("Дата")
#     breakfast = models.ForeignKey(MenuStructure, verbose_name="Завтрак", on_delete=models.DO_NOTHING)
#
#     def __str__(self):
#         return f"Меню на {self.date}"
#
#     class Meta:
#         verbose_name = "Меню"
#         verbose_name_plural = "Меню"


