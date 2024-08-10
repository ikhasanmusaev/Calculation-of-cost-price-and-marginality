from django.contrib import admin
from .models import TaxRate, MarketplaceCommission, Product


@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    list_display = ('rate',)
    list_filter = ('rate',)


@admin.register(MarketplaceCommission)
class MarketplaceCommissionAdmin(admin.ModelAdmin):
    list_display = ('category', 'fbs_rate', 'fbo_rate', 'fbo_rate')
    list_filter = ('category',)
    search_fields = ('category',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'purchase_price', 'desired_price', 'margin_percentage', 'category')
    list_filter = ('category', 'tax_rate')
    search_fields = ('name', 'category__category')
    readonly_fields = ('calculate_volume', 'calculate_delivery_cost')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'purchase_price', 'category', 'tax_rate')
        }),
        ('Ценообразование', {
            'fields': ('desired_price', 'margin_percentage')
        }),
        ('Логистика', {
            'fields': ('logistics_cost', 'logistics_quantity')
        }),
        ('Размеры', {
            'fields': ('height', 'length', 'width')
        }),
        ('Расчеты', {
            'fields': ('calculate_volume', 'calculate_delivery_cost')
        }),
    )

    def calculate_volume(self, obj):
        return f"{obj.calculate_volume():.2f} л"

    calculate_volume.short_description = "Объем товара"

    def calculate_delivery_cost(self, obj):
        return f"{obj.calculate_delivery_cost():.2f} руб."

    calculate_delivery_cost.short_description = "Стоимость доставки"
