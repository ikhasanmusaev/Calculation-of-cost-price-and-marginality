from rest_framework import serializers
from .models import Product, TaxRate, MarketplaceCommission


class ProductSerializer(serializers.ModelSerializer):
    tax_rate = serializers.PrimaryKeyRelatedField(
        queryset=TaxRate.objects.all(),
        required=False,
        help_text="ID выбранной налоговой ставки. Если не указано, налог не учитывается при расчете."
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=MarketplaceCommission.objects.all(),
        help_text="ID категории товара для определения комиссии маркетплейса."
    )

    class Meta:
        model = Product
        fields = [
            'name', 'purchase_price', 'logistics_cost', 'logistics_quantity',
            'tax_rate', 'desired_price', 'margin_percentage', 'category',
            'height', 'length', 'width'
        ]
        extra_kwargs = {
            'name': {'help_text': "Название товара"},
            'purchase_price': {'help_text': "Себестоимость закупки товара за 1 шт"},
            'logistics_cost': {'help_text': "Общая стоимость логистики за партию"},
            'logistics_quantity': {'help_text': "Количество товаров в партии для расчета логистики"},
            'desired_price': {'help_text': "Желаемая стоимость продажи. Можно ввести как произвольную сумму",
                              'required': False},
            'margin_percentage': {
                'help_text': "Процент маржинальности. Используется для расчета цены продажи, если не указана желаемая цена",
                'required': False},
            'height': {'help_text': "Высота товара для расчета объема и стоимости доставки"},
            'length': {'help_text': "Длина товара для расчета объема и стоимости доставки"},
            'width': {'help_text': "Ширина товара для расчета объема и стоимости доставки"},
        }

    def validate(self, data):
        if data.get('desired_price') is None and data.get('margin_percentage') is None \
                or data.get('margin_percentage') is not None and data.get('desired_price') is not None:
            raise serializers.ValidationError(
                "Необходимо указать либо желаемую цену (desired_price), либо процент маржинальности (margin_percentage)")
        return data


class ProductGetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category', read_only=True)

    class Meta:
        model = Product
        fields = ['category_name', 'name', 'desired_price', 'margin_percentage']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        logistics_cost_per_item = instance.logistics_cost / instance.logistics_quantity
        total_cost = float(instance.purchase_price + logistics_cost_per_item)

        if instance.tax_rate:
            total_cost += total_cost * instance.tax_rate.rate

        if instance.desired_price:
            selling_price = float(instance.desired_price)
        else:
            selling_price = float(instance.purchase_price) * instance.margin_percentage

        commission = instance.category
        fbs_commission = selling_price * commission.fbs_rate / 100
        fbo_commission = selling_price * commission.fbo_rate / 100
        dbs_commission = selling_price * commission.dbs_rate / 100

        volume = (instance.height * instance.length * instance.width) / 1000  # в литрах
        delivery_cost = volume * 50

        profit_per_item_fbs = selling_price - total_cost - fbs_commission - delivery_cost
        profit_per_batch = profit_per_item_fbs * instance.logistics_quantity

        representation['total_cost'] = round(total_cost, 2)
        representation['selling_price'] = round(selling_price, 2)
        representation['fbs_commission'] = round(fbs_commission, 2)
        representation['fbo_commission'] = round(fbo_commission, 2)
        representation['dbs_commission'] = round(dbs_commission, 2)
        representation['delivery_cost'] = delivery_cost
        representation['profit_per_item_fbs'] = round(profit_per_item_fbs, 2)
        representation['profit_per_batch'] = round(profit_per_batch, 2)
        return representation
