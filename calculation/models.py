from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class TaxRate(models.Model):
    rate = models.FloatField(
        choices=[(0.01, '1%'), (0.07, '7%'), (0.15, '15%'), (0.25, '25%')])


class MarketplaceCommission(models.Model):
    category = models.CharField(
        max_length=100,
        help_text="Название категории товара."
    )  # Так как в одном уровне, не стоит добавить модель
    fbs_rate = models.FloatField()
    fbo_rate = models.FloatField()
    dbs_rate = models.FloatField()


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        help_text="Название товара."
    )
    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Себестоимость закупки товара за 1 шт."
    )
    desired_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Желаемая стоимость продажи. Можно ввести как произвольную сумму."
    )
    margin_percentage = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
        help_text="Процент маржинальности. Используется для расчета цены продажи, если не указана желаемая цена."
    )

    # Logistic ========================================================
    logistics_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Общая стоимость логистики за партию."
    )
    logistics_quantity = models.PositiveIntegerField(
        help_text="Количество товаров в партии для расчета логистики."
    )

    # =================================================================
    tax_rate = models.ForeignKey(
        TaxRate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Выбранная налоговая ставка. Если не указано, налог не учитывается при расчете."
    )
    category = models.ForeignKey(
        MarketplaceCommission,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Категория товара для определения комиссии маркетплейса."
    )

    # Размеры
    height = models.FloatField(
        help_text="Высота товара для расчета объема и стоимости доставки."
    )
    length = models.FloatField(
        help_text="Длина товара для расчета объема и стоимости доставки."
    )
    width = models.FloatField(
        help_text="Ширина товара для расчета объема и стоимости доставки."
    )

    def calculate_volume(self):
        return (self.height * self.length * self.width) / 1000

    def calculate_delivery_cost(self):
        return self.calculate_volume() * 50  # 50 рублей за литр

    def __str__(self):
        return self.name
