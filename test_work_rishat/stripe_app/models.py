from django.db import models


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.IntegerField()

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField("Item")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def get_items(self):
        return Item.objects.filter(order__id=self.id)


class Discount(models.Model):
    coupon_id = models.CharField(max_length=64, null=False, blank=False)
    percent_off = models.IntegerField()

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    def __str__(self):
        return str(self.percent_off)

    def return_discounts(self):
        return [{'coupon': self.coupon_id}]
